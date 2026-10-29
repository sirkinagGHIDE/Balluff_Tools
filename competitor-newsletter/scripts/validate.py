#!/usr/bin/env python3
"""Validate digest run files against the BUILD_SPEC rules.

Exit code 0 when everything passes, 1 when any rule fails. Every failure line names
the file, the item id and the rule.

Rules (numbering matches BUILD_SPEC section 7; rule 0 is a structural pre-check):
  0  schema        run or item is malformed (missing field, wrong type, bad date)
  1  source        item has no source (basis=reported), or a source URL is not http(s)
  2  enum          competitor or category outside the enum, or competitor missing from config
  3  length        summary exceeds the word limit
  4  pricing       title or summary matches a product-pricing pattern
  5  part-number   title or summary matches a part-number pattern not in the allowlist
  6  duplicate     same id appears twice across runs and update_of is not set
  7  analysis      basis=analysis with zero sources
  8  event-date    event item lacks start_date, or start_date is before the run date
  9  digest        data/digest.js does not match a fresh bundle.py build
  10 sample-leak   a non-sample run contains an item with "sample": true

Usage:
    python scripts/validate.py                    # whole repo: data/items, data/sample, digest.js
    python scripts/validate.py data/sample        # a directory of run files
    python scripts/validate.py data/items/2026-10-16.json
    python scripts/validate.py tests/bad_fixtures/r09_digest_mismatch   # a repo-shaped root

A path counts as sample data when it sits under a directory named "sample", or when
--sample is passed. Explicit run files are also checked for duplicate ids against the
committed runs in data/items (non-sample) or data/sample (sample).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bundle  # noqa: E402

REPO_ROOT = bundle.REPO_ROOT
RULE_NAMES = {
    0: "schema",
    1: "source",
    2: "enum",
    3: "length",
    4: "pricing",
    5: "part-number",
    6: "duplicate",
    7: "analysis",
    8: "event-date",
    9: "digest",
    10: "sample-leak",
}
RUN_KEYS = {"run_date", "window_start_utc", "window_end_utc", "status", "source_failures", "items"}
ITEM_KEYS = {"id", "competitor", "category", "tags", "title", "summary", "basis",
             "fallback", "update_of", "sources", "sample"}
TAG_KEYS = ("technology", "industry", "application")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def fail(self, path: Path | str, item_id: str | None, rule: int, detail: str) -> None:
        self.failures.append(
            f"FAIL rule {rule} ({RULE_NAMES[rule]}): file={display(path)} item={item_id or '-'}: {detail}"
        )


def display(path: Path | str) -> str:
    p = Path(path).resolve()
    try:
        return p.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(p)


def parse_date(value) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_datetime(value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


class Rules:
    def __init__(self, root: Path) -> None:
        cfg = bundle.config_dir(root)
        raw = bundle.load_json(cfg / "rules.json")
        competitors = bundle.load_json(cfg / "competitors.json")["competitors"]
        self.competitor_enum = set(raw["competitors"])
        self.configured = {c["id"] for c in competitors}
        self.categories = set(raw["categories"])
        self.basis_values = set(raw["basis_values"])
        self.max_words = int(raw["summary_max_words"])
        self.pricing_always = [re.compile(p) for p in raw["pricing"]["always"]]
        self.pricing_currency = [re.compile(p) for p in raw["pricing"]["currency_amounts"]]
        self.part_patterns = [re.compile(p) for p in raw["part_numbers"]["patterns"]]
        self.allowlist = set(raw["part_numbers"]["allowlist"])


# ---------------------------------------------------------------- run checks

def check_run_shape(path: Path, run, rep: Report) -> bool:
    if not isinstance(run, dict):
        rep.fail(path, None, 0, "run file must be a JSON object")
        return False
    ok = True
    missing = RUN_KEYS - run.keys()
    if missing:
        rep.fail(path, None, 0, f"run missing keys: {sorted(missing)}")
        ok = False
    if parse_date(run.get("run_date")) is None:
        rep.fail(path, None, 0, "run_date must be YYYY-MM-DD")
        ok = False
    elif path.suffix == ".json" and path.stem != run["run_date"] and re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.stem):
        rep.fail(path, None, 0, f"file name {path.name} does not match run_date {run['run_date']}")
        ok = False
    for key in ("window_start_utc", "window_end_utc"):
        if key in run and parse_datetime(run.get(key)) is None:
            rep.fail(path, None, 0, f"{key} must be ISO-8601")
            ok = False
    if run.get("status") not in ("ok", "partial"):
        rep.fail(path, None, 0, "status must be 'ok' or 'partial'")
        ok = False
    failures = run.get("source_failures")
    if not isinstance(failures, list) or any(
        not isinstance(f, dict) or not {"competitor", "url", "error"} <= f.keys() for f in failures
    ):
        rep.fail(path, None, 0, "source_failures must be a list of {competitor, url, error}")
        ok = False
    elif run.get("status") == "partial" and not failures:
        rep.fail(path, None, 0, "status 'partial' requires at least one source_failures entry")
        ok = False
    if not isinstance(run.get("items"), list):
        rep.fail(path, None, 0, "items must be a list")
        ok = False
    return ok


def check_item_shape(path: Path, item, rep: Report) -> bool:
    if not isinstance(item, dict):
        rep.fail(path, None, 0, "item must be a JSON object")
        return False
    item_id = item.get("id") if isinstance(item.get("id"), str) else None
    ok = True

    def bad(detail: str) -> None:
        nonlocal ok
        rep.fail(path, item_id, 0, detail)
        ok = False

    missing = ITEM_KEYS - item.keys()
    if missing:
        bad(f"item missing keys: {sorted(missing)}")
        return False
    if not isinstance(item["id"], str) or not SHA1_RE.match(item["id"]):
        bad("id must be a 40-char lowercase sha1 hex string")
    for key in ("title", "summary", "competitor", "category", "basis"):
        if not isinstance(item[key], str) or not item[key].strip():
            bad(f"{key} must be a non-empty string")
    tags = item["tags"]
    if not isinstance(tags, dict) or any(
        not isinstance(tags.get(k), list) or not all(isinstance(t, str) for t in tags[k]) for k in TAG_KEYS
    ):
        bad("tags must have technology, industry and application lists of strings")
    if not isinstance(item["fallback"], bool):
        bad("fallback must be true or false")
    if not isinstance(item["sample"], bool):
        bad("sample must be true or false")
    if item["update_of"] is not None and (not isinstance(item["update_of"], str) or not SHA1_RE.match(item["update_of"])):
        bad("update_of must be null or a sha1 id")
    if not isinstance(item["sources"], list):
        bad("sources must be a list")
    else:
        for src in item["sources"]:
            if not isinstance(src, dict) or not {"url", "publisher", "published_date", "retrieved_utc"} <= src.keys():
                bad("each source needs url, publisher, published_date, retrieved_utc")
            elif parse_date(src["published_date"]) is None:
                bad(f"source published_date must be YYYY-MM-DD: {src['published_date']!r}")
            elif parse_datetime(src["retrieved_utc"]) is None:
                bad(f"source retrieved_utc must be ISO-8601: {src['retrieved_utc']!r}")
    # A missing event block on an event item is reported by rule 8 (no start_date).
    if "event" in item and item.get("category") != "event":
        bad("event block is allowed only when category is 'event'")
    return ok


def scan_text(item: dict) -> str:
    return f"{item.get('title', '')}\n{item.get('summary', '')}"


def check_item_rules(path: Path, run: dict, item: dict, rules: Rules, is_sample: bool, rep: Report) -> None:
    item_id = item["id"]
    basis = item.get("basis")
    sources = item.get("sources") or []

    # Rule 1 and 7: sources.
    if not sources:
        if basis == "analysis":
            rep.fail(path, item_id, 7, "basis is 'analysis' but the item has zero sources")
        else:
            rep.fail(path, item_id, 1, "item has no source")
    for src in sources:
        url = src.get("url", "") if isinstance(src, dict) else ""
        parsed = urlparse(url if isinstance(url, str) else "")
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            rep.fail(path, item_id, 1, f"source URL is not http(s): {url!r}")

    # Rule 2: enums and config.
    comp = item.get("competitor")
    if comp not in rules.competitor_enum:
        rep.fail(path, item_id, 2, f"competitor {comp!r} is outside the enum")
    elif comp not in rules.configured:
        rep.fail(path, item_id, 2, f"competitor {comp!r} is missing from config/competitors.json")
    if item.get("category") not in rules.categories:
        rep.fail(path, item_id, 2, f"category {item.get('category')!r} is outside the enum")
    if basis not in rules.basis_values:
        rep.fail(path, item_id, 0, f"basis {basis!r} must be one of {sorted(rules.basis_values)}")

    # Rule 3: length.
    words = len(str(item.get("summary", "")).split())
    if words > rules.max_words:
        rep.fail(path, item_id, 3, f"summary has {words} words (max {rules.max_words})")

    # Rule 4: pricing. Company-level money figures are allowed in the financial category.
    text = scan_text(item)
    patterns = list(rules.pricing_always)
    if item.get("category") != "financial":
        patterns += rules.pricing_currency
    for pat in patterns:
        m = pat.search(text)
        if m:
            rep.fail(path, item_id, 4, f"pricing pattern matched {m.group(0)!r} ({pat.pattern})")
            break

    # Rule 5: part numbers.
    for pat in rules.part_patterns:
        hits = [m.group(0) for m in pat.finditer(text) if m.group(0) not in rules.allowlist]
        if hits:
            rep.fail(path, item_id, 5, f"part-number pattern matched {hits[0]!r} ({pat.pattern}); "
                                       "use the family name or add it to rules.json allowlist")
            break

    # Rule 8: events.
    if item.get("category") == "event":
        event = item.get("event") if isinstance(item.get("event"), dict) else {}
        start = parse_date(event.get("start_date"))
        run_day = parse_date(run.get("run_date"))
        if start is None:
            rep.fail(path, item_id, 8, "event item lacks a valid start_date")
        elif run_day and start < run_day:
            rep.fail(path, item_id, 8, f"event start_date {start} is before run date {run_day}")
        end_raw = event.get("end_date")
        if start and end_raw not in (None, ""):
            end = parse_date(end_raw)
            if end is None or end < start:
                rep.fail(path, item_id, 0, f"event end_date {end_raw!r} is invalid or before start_date")

    # Rule 10: sample leak.
    if not is_sample and item.get("sample") is True:
        rep.fail(path, item_id, 10, "non-sample run contains an item with \"sample\": true")


# ------------------------------------------------------------ orchestration

def is_sample_path(path: Path) -> bool:
    resolved = path.resolve()
    try:
        parts = resolved.relative_to(REPO_ROOT).parts
    except ValueError:
        parts = resolved.parts
    return "sample" in [part.lower() for part in parts[:-1]]


def load_run(path: Path, rep: Report):
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        rep.fail(path, None, 0, f"cannot read JSON: {exc}")
        return None


def validate_runs(paths: list[Path], rules: Rules, sample: bool, rep: Report,
                  prior: list[Path] | None = None) -> int:
    """Validate run files. `prior` runs only feed the duplicate-id check."""
    seen: dict[str, tuple[Path, str | None]] = {}
    targets = {p.resolve() for p in paths}

    for p in sorted({q.resolve() for q in prior or []} - targets):
        run = load_run(p, Report())
        items = run.get("items") if isinstance(run, dict) else None
        for item in items if isinstance(items, list) else []:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                seen.setdefault(item["id"], (p, item.get("update_of")))

    count = 0
    for path in sorted(targets):
        run = load_run(path, rep)
        if run is None or not check_run_shape(path, run, rep):
            continue
        for item in run["items"]:
            count += 1
            if not check_item_shape(path, item, rep):
                continue
            check_item_rules(path, run, item, rules, sample, rep)
            # Rule 6: duplicates across runs (and within one run).
            item_id = item["id"]
            if item_id in seen and not item.get("update_of"):
                first = seen[item_id][0]
                rep.fail(path, item_id, 6, f"duplicate id (first seen in {display(first)}) and update_of is not set")
            seen.setdefault(item_id, (path, item.get("update_of")))
    return count


def validate_root(root: Path, rep: Report) -> int:
    rules = Rules(root)
    items_dir, sample_dir = root / "data" / "items", root / "data" / "sample"
    n = validate_runs(list(items_dir.glob("*.json")), rules, False, rep)
    n += validate_runs(list(sample_dir.glob("*.json")), rules, True, rep)
    # Rule 9.
    digest = root / "data" / "digest.js"
    current = digest.read_text(encoding="utf-8").replace("\r\n", "\n") if digest.is_file() else None
    if current is None:
        rep.fail(digest, None, 9, "data/digest.js is missing; run python scripts/bundle.py")
    elif current != bundle.render(root):
        rep.fail(digest, None, 9, "data/digest.js does not match a fresh bundle.py build; run python scripts/bundle.py")
    return n


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate competitor digest data.")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--sample", action="store_true", help="treat explicit paths as sample data")
    args = parser.parse_args(argv)

    rep = Report()
    total = 0
    if not args.paths:
        total = validate_root(REPO_ROOT, rep)
    for raw in args.paths:
        path = raw.resolve()
        if not path.exists():
            rep.fail(path, None, 0, "path does not exist")
        elif path.is_dir() and (path / "data").is_dir():
            total += validate_root(path, rep)
        else:
            files = sorted(path.glob("*.json")) if path.is_dir() else [path]
            sample = args.sample or is_sample_path(files[0] if files else path)
            prior_dir = REPO_ROOT / "data" / ("sample" if sample else "items")
            total += validate_runs(files, Rules(REPO_ROOT), sample, rep, list(prior_dir.glob("*.json")))

    for line in rep.failures:
        print(line)
    if rep.failures:
        print(f"\n{len(rep.failures)} failure(s).", file=sys.stderr)
        return 1
    print(f"OK: {total} item(s) checked, all rules pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
