---
backtest: N4-01_breakout-drift-lasts_1d_oos_sized
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9329 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5966 | above 0 | yes |
| Mean daily return | 0.0009341 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4986 | above 0 | yes |
| Calmar | 0.7327 | above 0.75 | no |
| Trades per bar | 0.153 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_sized/N4-01_breakout-drift-lasts_1d_oos_sized`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
