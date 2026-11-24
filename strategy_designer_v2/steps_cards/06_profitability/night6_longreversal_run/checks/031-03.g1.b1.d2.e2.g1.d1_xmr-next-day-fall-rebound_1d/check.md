---
backtest: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d
data: XMR as XMRUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.064 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6236 | above 0 | yes |
| Mean daily return, on days in a position | 0.001057 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.928 | above 0 | yes |
| Calmar | 1.331 | above 0.75 | yes |
| Trades per day | 0.3235 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.216 % |
| Yearly return | +24.7 % (over 7.94 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
