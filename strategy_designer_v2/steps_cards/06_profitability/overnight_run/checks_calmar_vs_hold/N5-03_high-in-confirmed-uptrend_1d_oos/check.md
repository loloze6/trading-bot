---
backtest: N5-03_high-in-confirmed-uptrend_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7037 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3352 | above 0 | yes |
| Mean daily return | 0.0007826 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1381 | above 0 | yes |
| Calmar | 0.4484 | above -0.01528 | yes |
| Trades per bar | 0.1164 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N5-03_high-in-confirmed-uptrend_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
