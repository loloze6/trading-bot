---
backtest: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d
data: XMR as XMRUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.816 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4145 | above 0 | no |
| Mean daily return, on days in a position | 0.001715 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.504 | above 0 | yes |
| Calmar | 8.733 | above 0.75 | yes |
| Trades per day | 0.3143 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.750 % |
| Yearly return | +48.2 % (over 0.67 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_longreversal_run/unseen_2016_2017/backtests/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
