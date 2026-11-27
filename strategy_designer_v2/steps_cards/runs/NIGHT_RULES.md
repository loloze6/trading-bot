# Night rules: how a research night runs (standing; each night's run file says only what is new)

Written 2026-11-24 from nights 4 to 6 (`NIGHT4_RUN.md`, `RETEST_RUN.md`, `NIGHT6_RUN.md`) and next steps 3e, 3f and 3g.
A night's run file (`NIGHTn_RUN.md`) gives its purpose and expected outcomes, its sessions (run, theme or brief, bar,
budget) and what changed since the last night; everything else is here.

## Before the night (the designer)
1. The night's run file written: purpose, expected outcomes, sessions, budgets (set in each session's first message,
   never changed during the night).
2. Each session starts from the working branch, on its own branch `night<n>-<name>`.
3. **A watched pilot before the night when a step changed since the last night** (the operator, 2026-11-25, after night
   7 lost most of its turns to a ranking rule nobody had run in a loop): the changed chain runs once on one theme, a
   small budget (about 15 USD), during the day, with pass criteria written before it starts (`PILOT_CHAIN_RUN.md` is
   the first); the night starts only when every criterion passes, or a failure is fixed and its part rerun.
4. **Brief numbers (3e):** the operator's rule, still to decide. Until then the morning merge reports a number used
   twice (`night_merge`) and the reading names both briefs by their full file name.

## During the night (each session)
1. `run_brief --theme "<theme>" --run night<n>_<name>_run --budget <USD>` (or a brief file).
2. **Long jobs run as tracked background tasks, never detached (3f).** A detached process (`setsid nohup`) dies when the
   cloud reclaims an idle session's container (night 6: twice). A tracked task keeps the session attached; it is cut
   after 2 hours, so the session starts it with the longest timeout and, on its end notification, resumes the loop
   (`loop.py --run <run> --python <venv> --budget <the session's budget>`): the loop resumes from its files, an idea
   cut mid-run is finished first. **The budget must be given again:** the loop keeps none in the run's files and has no
   limit without `--budget`; with it, it counts the run's whole spend (night 8: resumed without it, C reached 42.4 of
   40 USD before it stopped its loop itself).
3. A stop on "the model service refused a call" (the usage limit) is resumed after the limit's reset: the session
   schedules its own wake-up.
4. Commits and pushes on the session's branch along the way (after each idea at most every 30 minutes), and at the end.
5. No new idea after 07:00 UTC (09:00 at most if the usage limit cost time); an idea started is finished.
6. Discoveries (an idea off its brief's theme, topic 50) become briefs inside the run, by the loop: nothing to do.

## In the morning (the designer)
1. **Merge with `night_merge` (3g):** `orchestration/night_merge/helper/night_merge.py <branches> --python <venv>`, the
   branches in the order the sessions ended. It merges by one rule per shared file, stops on what no rule covers,
   rebuilds the register, reports brief numbers used twice and runs both test suites. Never by hand.
2. The reading, in the night's run file: which expected outcome happened; per brief, its answer (`common/theme.md`):
   the theme found real, not real, or open (budget ended), the turn at which it was answered and the spend after it;
   the discoveries and the briefs they became; confirmed books,
   paying books, portfolio candidates; the cost. Counts, not impressions.
3. **What the night adds to the portfolio (next steps A8, 2026-11-27):** the reading of a run or of a batch carries
   the table of `orchestration/combine/helper/addition.py --runs <the night's runs> --name night<n>` (the portfolio
   built by rule with and without the night's candidates, on the same coin-days: Sharpe, yearly return, worst fall, the
   return at a 20 % fall, each calendar year, the strategies that entered or left), quoted from
   `orchestration/combine/additions/night<n>.md`. A run or batch is judged by this table; the count of confirmed and
   profitable strategies stays in the reading as information.
4. Step back before anything else: what the night shows, and the one change a practitioner would make; added to the
   next-step list.
