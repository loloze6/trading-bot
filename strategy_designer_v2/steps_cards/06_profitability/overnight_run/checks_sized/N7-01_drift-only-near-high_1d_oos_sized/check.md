---
backtest: N7-01_drift-only-near-high_1d_oos_sized
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.263 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.9266 | above 0 | yes |
| Mean daily return | 0.0008665 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8226 | above 0 | yes |
| Calmar | 1.417 | above 0.75 | yes |
| Trades per bar | 0.1514 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_sized/N7-01_drift-only-near-high_1d_oos_sized`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
