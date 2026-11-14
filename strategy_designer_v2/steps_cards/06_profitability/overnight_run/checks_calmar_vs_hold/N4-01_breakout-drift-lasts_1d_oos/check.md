---
backtest: N4-01_breakout-drift-lasts_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5769 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2406 | above 0 | yes |
| Mean daily return | 0.001234 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2195 | above 0 | yes |
| Calmar | 0.189 | above -0.04838 | yes |
| Trades per bar | 0.1715 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-01_breakout-drift-lasts_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
