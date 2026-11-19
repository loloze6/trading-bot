# unseen_test: validation (2026-11-18)

**Purpose:** show that the function, called by `run_idea`, gives exactly what the steps gave when called by hand on
the same plan and periods (`runs/UNSEEN_RUN.md`). Expected: identical files; anything else is a defect.

**How:** `run_idea` on `02_ideation/night_rsi_run/ideas/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week.md`
with `--run night_rsi_run` (resumed: every step's output existed). Then the function's files compared with
`unseen_run`'s for the same idea.

| Check | Result |
|---|---|
| Steps 3, 4, 5 and the 7 lines | skipped, outputs exist (journal); step 6 and the chart files called, as on every resume |
| unseen_test | called once, 40 s, 0 USD, no model call |
| Engine files (bars, trades, metrics, forecast distribution), 2026 | 24 of 24 identical |
| Engine files, 2016-17 | 48 of 48 identical |
| Step 5 result.json, both periods | identical |
| Step 6 result.json, both periods | identical |
| Row | "unseen dates: unseen_2016_2017: holds; unseen_2026: holds", as the hand reading |
| Tests of its own logic | 3 (the holds rule, the periods, the files and the resume) |

**Outcome:** as expected. The proof's files were then removed (the idea's unseen result is `runs/UNSEEN_RUN.md`'s;
keeping a second copy in `night_rsi_run` would put one result in two places).
