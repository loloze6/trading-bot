---
backtest: N2-01_weekday-of-coming-bar_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5128 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8814 | above 0 | no |
| Mean daily return | -0.0001237 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8601 | above 0 | no |
| Calmar | -0.2068 | above -0.01528 | no |
| Trades per bar | 0.06577 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N2-01_weekday-of-coming-bar_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
