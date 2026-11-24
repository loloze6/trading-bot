---
backtest: 031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d
data: XMR as XMRUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7771 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3371 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008055 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6103 | above 0 | yes |
| Calmar | 0.487 | above 0.75 | no |
| Trades per day | 0.8278 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.975 % |
| Yearly return | +24.8 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
