# Leads verification: brief (approved by the operator, 2026-11-04)

## Purpose
During the guided tour, an inspector wrote, for every stop, a section "(2) Legacy or simplifiable":
parts that look unused, unread, kept for nothing, or simplifiable. The tour's opening prompt says:
"These are leads, not facts: a separate agent verifies them by search after the tour."
You are that verifier. You check each lead against the code by search and report a verdict with
evidence. You decide nothing and change nothing: the direction session leads the post-tour
analysis and decides what happens to each lead.

## Repo and flag set
Repo: /home/user/trading-bot. SR = strategy-research/, TB = trading-bot/,
RP = SR/workflow/run_phase1_research.py, RC = SR/workflow/run_campaign.py.
Code: master 78790e5f (2026-10-28), the code the tour read.
FLAG SET TO JUDGE UNDER (the tour's, the operator's PC): every flag under `orchestrator:` in
SR/config/campaign_config.yaml (listed in SR/config/feature_flag_register.yaml) is ON, except
three that are OFF: `deviation_gate`, `zero_trade_windows_not_computed`, `extra_cards_at_1a`.
This checkout's committed campaign_config.yaml has most flags `enabled: false`; IGNORE those values
and reason under the tour's set above. Where a verdict depends on a non-flag config value, say so.
Not in this checkout: SR/runs/ after run_060 (so run_102's files), the operator's live queue
(committed campaign_queue.yaml and SR/campaign_record/ stop at run_097, 2026-10-20). A lead that
needs those is "NOT CHECKABLE HERE".

## What to do, per lead
1. Read the lead in the stop file's "## Inspector notes" -> "(2) Legacy or simplifiable" section.
   Read the stop's Speech only if you need context. Do not edit stop files.
2. Restate the lead in one line (no dates).
3. Verify by search: grep for every reader/writer/caller, including indirect access (string keys
   in YAML/JSON configs, getattr/dict lookups by name, dynamic imports, skill/prompt text that tells
   an AI to read it, templates, schemas, CI workflows (.github/), run_tests.py, tests/, scripts,
   docs that are operator procedure). Check the call path is reachable under the flag set above.
   Line numbers in a lead may have drifted: use the real ones.
4. Verdict, exactly one of:
   - CONFIRMED: the lead's factual claim holds (unused / unread / unreachable / duplicated as stated).
   - PARTLY: part holds, part does not; say which.
   - REFUTED: a live reader, writer or use exists; cite it.
   - NOT CHECKABLE HERE: needs run data or the PC's state.
   - DESIGN CALL: the lead is a simplification or standardisation suggestion, not a fact; verify
     its factual premise only and say whether the premise holds.
5. Removal footprint (for CONFIRMED/PARTLY): what removing or simplifying it would touch: files,
   tests that reference it, schemas, docs, configs. Count tests that mention it.
6. Evidence: the exact searches you ran (pattern and scope) and their hit counts, plus file:line
   for each relevant hit. Say what you did NOT check.

## Output
Write ONLY your batch file guided_tour/_post_tour/batch_<NN>.md:

# Batch NN: stops <list>
| ID | Lead (one line) | Verdict | Evidence (searches, hits, file:line) | Removal footprint |
|---|---|---|---|---|
One row per lead. ID = <stop>-<lead number as numbered in the inspector's section 2>, e.g. 05b-3.
For itinerary parked leads use P-1, P-2, ... in the order listed.
After the table: "## Not checked" (anything you could not verify and why).

## Hard rules
- Read-only everywhere except your batch file. No git commands that change anything; no runs,
  backtests, tests (no pytest, no run_tests.py), pipeline scripts, hooks or servers. python3 only
  for read-only searching/counting.
- Never open, list or glob TB/local_data/ or anything named holdout_sealed;
  never open SR/campaign_record/composite/ or SR/quarantine/.
- Never write any date from SR/config/campaign_data_policy.yaml, any protocol window label, or any
  date range. Fold ids (A-D) and years only.
- Never copy secrets; write [REDACTED].
- Do not propose fixes or designs. Facts and evidence only.
