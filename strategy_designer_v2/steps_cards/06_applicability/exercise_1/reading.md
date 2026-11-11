# Exercise 1: step 6 built and run

**What ran.** `helper/make_assessment.py` with `helper/rule.yaml` (branch 3's values, without the deflated Sharpe and the drawdown ceiling). Code only: no model, no cost. Log: `run_log.txt`.

## The tests (hand-made records, not market data)
4 of 4 pass (`helper/test_make_assessment.py`):
- **A steady winning book** is "worth acting on", and its Sharpe, Sharpe minus holding, mean daily return and trade count match an independent recomputation.
- **A losing book** fails the Sharpe and daily-return bars.
- **One bad window** fails Calmar and the leave-one-window-out bar; the deepest fall and the lowest Sharpe match the independent recomputation.
- **A book with no trades** fails the frequency bar.

## The gate (`gate/`)
The 6 ideas of the full-data run are inconclusive: all 6 give "not assessed: the verdict is inconclusive". Right.

## Real records, exercise mode (`full_data/`, `hourly/`)
`--any-verdict` assesses them anyway, to test the arithmetic on real books. All 16 are "not worth acting on", as expected for ideas that are not real.

| Idea | Sharpe | Holding's | Calmar | Deepest fall | Failed bars |
|---|---|---|---|---|---|
| 002-03 daily, price above its 200-day average (6 coins, 8 years) | 0.51 | 0.57 | 0.14 | 83 % | beats holding; Calmar |
| 002-01 / 002-05 daily, short average above long | 0.38 | 0.57 | 0.00 | 93 % | beats holding; Calmar |
| short-side daily books (002-02, -04, -06) | -0.41 to -0.52 | 0.57 | below 0 | 94 to 98 % | five of six |
| 001 RSI hourly (BTC, ETH) | -1.6 to -2.9 | 0.07 | below 0 | 86 to 98 % | five of six: the churn of about 600 trades a window |
| 002-03 hourly, price above its average (BTC) | 0.73 | 0.18 | 0.63 | 42 % | Calmar only |

**Checks on the real records:**
- **Forced closes are excluded:** on 002-03 daily, the engine counted 2,228 trades, 331 of them closed on a window's last bar; 1,897 are counted.
- **Duplicates give identical assessments:** 002-01 = 002-05 and 002-02 = 002-06, as their books are the same.
- **The numbers read sensibly against the books:** the hourly RSI books lose on their trading, as seen in the hourly run's review.

**Status.** "Done when" is met: the tests pass, every real assessment follows the rule, the gate holds.

**Not yet tested end to end:** a "worth acting on" on a real backtest. Only the hand-made records reach it. Closest real book: 002-03 hourly, which fails on Calmar alone (0.63 against 0.75).
