---
backtest: N7-01_drift-only-near-high_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9097 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5905 | above 0 | yes |
| Mean daily return | 0.001268 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5147 | above 0 | yes |
| Calmar | 0.8017 | above -0.06904 | yes |
| Trades per bar | 0.1528 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N7-01_drift-only-near-high_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
