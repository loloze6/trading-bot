# Review of the verdicts in this folder

**Where they come from.** The current helper (with the situation check), run on the 29 daily plans of `../../03_test_plan/plans/` (rewritten with symmetric criteria) and their records in `../../04_backtest/backtests/`. A second run, side by side, is `../exercise_8/`. Log: `run_log.txt`. Cost: 0.94 USD (the second run: 1.14).

| | count |
|---|---|
| confirmed | 0 |
| rejected | 0 |
| inconclusive | 13 |
| mismatch | 0 |
| no verdict: untestable or missing-components | 14 |
| no verdict: refused by the engine (003-01, 003-02) | 2 |

The reading, plan by plan, is in `../exercise_8/reading.md`.

**On the default data, no idea shows evidence either way.** Every |t| is below 1.4. The previous six "rejected" verdicts rested on t between -0.76 and +0.24; with a reject that needs t ≤ -2 against the idea, they are inconclusive, which is what those numbers say. The default data is BTC (plus ETH for the RSI ideas), daily bars, fold A: about 730 bars per coin. More data is the operator's lever, in steps 1 and 2 (the bar size, the fold).
