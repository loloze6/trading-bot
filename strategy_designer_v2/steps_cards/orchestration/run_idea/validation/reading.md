# run_idea: validation on the fixed input (2026-11-16)

**Input**: the 002-03 repair from 7.d (`07_common/validation_run/ideas/...d1_above-average-drift-near-highs.md`,
brief 002), run `demo_run`.

**First full call** (with the journal; step 3's plan came from an earlier call of the same run, interrupted before
the journal existed, so its cost, about 0.3 USD, is not counted):

| Step | What happened | USD | Minutes |
|---|---|---|---|
| 3 | skipped: the plan exists | 0 | 0 |
| 4 | backtest, 6 coins (XMR 23 of 24 windows, XRP 22: the engine's warm-up defect) | 0 | 11.6 |
| 5 | **not observable** (t +1.22): the plan asks about 860 cases in all; the record gives 827 | 0.14 | 0.6 |
| 6 | profitable enough | 0 | 0.1 |
| 7 | 7.a, 7.e, 7.g ran (4 ideas); 7.b, 7.c, 7.d declined: entry condition not met; 7.f not active | 0.91 | 2.8 |

**Against the validation run** (inconclusive, t 0.61): step 3 wrote a new plan, with the current rules (times in real
time, the supporting check counting), whose minimum count the record misses by a few windows. The chain reproduces
what the steps give; it does not reproduce an earlier plan (step 3 is a model call). The done-when criterion says so.

**Second and third calls**: every step skipped except step 6 (code, 2 seconds); no model call, no backtest; the row's
cost stays the idea's total in the run (from the journal).

**Fixed by the test**: a resumed run copied its brief onto itself (it found its own copy first); the row showed the
last call's cost (0 after a resume) instead of the idea's total; the journal said "called" for a line that declined.

**Met**: every status in the row is the step's own file; the lines that ran are those whose entry held; every file is
in its place and in the journal; a second call makes no model call and no backtest.

**Seen on the way, not the function's**: the engine's warm-up defect (parked) now changes a verdict: a plan whose
minimum count is close to the most the data can give becomes "not observable" when a few windows do not run.
