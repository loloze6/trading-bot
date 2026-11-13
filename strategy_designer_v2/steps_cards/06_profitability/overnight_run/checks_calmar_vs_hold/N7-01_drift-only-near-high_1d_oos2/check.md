---
backtest: N7-01_drift-only-near-high_1d_oos2
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds B, C
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.8 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.281 | above 0 | yes |
| Mean daily return | 0.00485 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.04 | above 0 | yes |
| Calmar | 3.666 | above 3.372 | yes |
| Trades per bar | 0.1945 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N7-01_drift-only-near-high_1d_oos2`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
