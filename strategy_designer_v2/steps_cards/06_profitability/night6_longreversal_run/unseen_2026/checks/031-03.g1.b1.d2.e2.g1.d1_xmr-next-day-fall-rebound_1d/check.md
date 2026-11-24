---
backtest: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d
data: XMR as XMRUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.383 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6502 | above 0 | yes |
| Mean daily return, on days in a position | 0.001659 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6317 | above 0 | yes |
| Calmar | 3.363 | above 0.75 | yes |
| Trades per day | 0.2991 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.371 % |
| Yearly return | +39.0 % (over 0.87 years) |
| Days in a position | 60 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_longreversal_run/unseen_2026/backtests/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
