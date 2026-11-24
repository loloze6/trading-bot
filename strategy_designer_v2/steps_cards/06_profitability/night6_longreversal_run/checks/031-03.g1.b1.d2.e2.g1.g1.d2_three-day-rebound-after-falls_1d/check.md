---
backtest: 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d
data: XMR as XMRUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5804 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1404 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009039 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4806 | above 0 | yes |
| Calmar | 0.333 | above 0.75 | no |
| Trades per day | 0.4714 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.626 % |
| Yearly return | +17.6 % (over 7.94 years) |
| Days in a position | 88 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
