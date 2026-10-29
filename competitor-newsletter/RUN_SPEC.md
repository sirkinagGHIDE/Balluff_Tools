# Competitor Newsletter — WEEKLY RUN

You run in a fresh session with no memory of prior runs. The repository is your only state.

## 1. Load
1. Clone `<ORG>/<REPO>`.
2. Read config/competitors.json, config/rules.json, data/state.json, RUN_SPEC.md.
3. Run `python scripts/validate.py` on the existing data before changing anything. If it fails, stop and report. Do not build on a broken state.

## 2. Window
- window_start = state.last_run_utc. If absent, use now − 7 days.
- window_end = now.
- If the window exceeds 14 days (missed runs), cover the full window and note it in your final report.

## 3. Collect
For each of: ifm, Keyence, Turck, Banner, SICK, Pepperl+Fuchs:
- Check every configured source first, then search the open web: press releases, newsroom, trade press, investor-relations/annual reports, event and trade-show listings.
- Include only items whose publication date falls inside the window. Take the date from the source page itself, not a search snippet.
- If the publication date cannot be established, exclude the item and list it in the report.
- Events are the exception: include events occurring within the next 90 days that are not already listed in a prior run.
- Record every source that errors or cannot be reached in source_failures, then continue.
- Log-in-only or paywalled content: skip it and list it. Never attempt access.

## 4. Write items
- Follow the schema in BUILD SPEC §5 exactly.
- Summary rules:
  - ≤80 words, original wording, no quotation longer than 15 words.
  - Lead with what it is and why it matters to a sales conversation.
- Never include product pricing or orderable part numbers. Product family names are fine.
- Financial: only figures from a cited disclosure. Label parent-level figures (Banner → Fortive). Never estimate, extrapolate, or annualize.
- Every claim must be traceable to a cited URL. Anything beyond what the sources state goes in an item with basis = "analysis".
- Deduplicate:
  - Skip any item whose id is in state.seen_ids, or whose title clearly matches a prior item.
  - If a prior story has materially new information, include it with update_of = prior id.
- Competitor summary:
  - Write ONE competitor_summary item for each competitor with at least one reported item this run (new_product, event, financial, or reported strategy). A competitor with none gets no summary; the §5 fallback covers it.
  - Title: "<Competitor>: week of <run_date as Mon D, YYYY>". The title-match dedup rule above does not apply to summaries.
  - Summary: 2–3 sentences, ≤80 words, on what the competitor did this week and the one point a sales rep should take from it. State only what this run's cited items say.
  - basis = "reported", fallback = false, update_of = null. tags = the union of the tags on that competitor's items this run.
  - sources: first, the competitor's first configured newsroom URL with the fragment `#digest-summary-<run_date>` appended (publisher = the competitor, published_date = run_date). This gives the summary its own id (the sha1 of that URL), since it cites the same URLs as its items. Then add the primary source of each of that competitor's items this run.

## 5. No-news fallback
If a competitor has zero reported items in the window:
- Write ONE strategy item: basis = "analysis", fallback = true.
- Build it only from cited public sources of any date, preferring the last 12 months. Cover a technology, application, or industry theme.
- If no citable basis exists, write: "No new public activity this period." Cite the sources checked.
- Never write an uncited claim to fill space.

## 6. Commit
1. Write data/items/<run_date>.json. Set status = "partial" if source_failures is non-empty.
2. Update data/state.json: last_run_utc, last_run_status, append new ids to seen_ids.
3. Run `python scripts/bundle.py`, then `python scripts/validate.py`.
4. If validation fails:
   - Correct or remove only the offending items and rerun.
   - If it still fails, DO NOT COMMIT. Report the failure with file, item id, and rule.
5. Commit everything in one commit to main: `digest: <run_date> (<n> items, <status>)`. Push.
6. Never modify site code, config, scripts, or either formatting repo during a run.

## 7. Final report
- Item counts per competitor and category.
- Competitors that used the fallback, and whether it had a citable basis.
- Source failures, excluded undated items, skipped login/paywalled sources.
- Items removed during validation and why.
- Commit hash, or the reason nothing was committed.
