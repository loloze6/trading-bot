# Leads verification, pass 2: independent re-check (approved by the operator, 2026-11-04)

Read BRIEF.md in this folder first: same repo, same flag set (all on except `deviation_gate`,
`zero_trade_windows_not_computed`, `extra_cards_at_1a`), same checkout limits, same hard rules.

## Your job
Pass 1 gave each inspector lead a verdict. A CONFIRMED or PARTLY verdict may later justify removing
or simplifying code, so each one gets an independent, adversarial re-check. Your goal is to REFUTE
it: find what pass 1 missed.

For every row with verdict CONFIRMED or PARTLY in your batch file(s):
1. Read the lead itself in the stop file's inspector section (2), and verify it FROM SCRATCH before
   reading pass 1's evidence, so you are not anchored on it.
2. Hunt for missed uses: string-keyed access (YAML/JSON keys read via dict lookups, config.get,
   schema properties), getattr/importlib/dynamic dispatch, skill and prompt text (SR/workflow_artifacts/,
   skills, templates, handoffs) that tells an AI to read or write it, tests (SR/tests, TB/tests),
   CI (.github/), run_tests.py, operator procedures (RUNBOOK, docs), the run viewer, tools run by
   hand (CLI entry points), the trading-bot side (TB/) as well as SR. Check reachability under the
   flag set.
3. Then compare with pass 1's evidence and removal footprint.
4. Verdict for the row:
   - UPHELD: you found nothing pass 1 missed; the claim stands as pass 1 stated it.
   - NARROWED: the claim holds only in part (say exactly which part survives).
   - OVERTURNED: a live use exists (cite it); the lead does not hold.
   - FOOTPRINT CORRECTED: the verdict stands but the removal footprint was incomplete (list what
     was missing).

## Output
Write ONLY your file pass2_<NN>.md in this folder (NN given in your task). Do not edit batch files
or stop files.

# Pass 2, batch(es) <NN>
| ID | Pass-1 verdict | Pass-2 verdict | What pass 1 missed / new evidence (file:line, searches, hits) |
|---|---|---|---|

Then "## Not checked". Facts and evidence only, no proposals, no dates.
