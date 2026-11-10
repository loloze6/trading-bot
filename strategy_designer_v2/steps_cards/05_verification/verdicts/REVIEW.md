# Review of the verdicts in this folder

**Where they come from.** These are exercise 6's verdicts: the current helper (prompt, record description and conventions), run on the 29 daily plans of `../../03_test_plan/plans/` and their records in `../../04_backtest/backtests/`. The run before it (exercise 5) gave the same status for every plan. Log: `run_log.txt`. Cost: 0.91 USD.

| | count |
|---|---|
| confirmed | 0 |
| rejected | 6 |
| inconclusive | 9 |
| no verdict (untestable, missing-components, refused by the engine) | 14 |

The reading, plan by plan, is in `../exercise_6/reading.md`.

**On the default data, nothing is confirmed.** The default is BTC (plus ETH for the RSI ideas), daily bars, fold A. Most inconclusive verdicts rest on small samples. More data (another fold, hourly bars set in the brief or the idea) is the operator's lever, in the earlier steps.
