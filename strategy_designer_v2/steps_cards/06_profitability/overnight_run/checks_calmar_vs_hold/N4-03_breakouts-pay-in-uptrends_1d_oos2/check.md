---
backtest: N4-03_breakouts-pay-in-uptrends_1d_oos2
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds B, C
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.189 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3837 | above 0 | no |
| Mean daily return | 0.002055 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2981 | above 0 | yes |
| Calmar | 1.22 | above 3.419 | no |
| Trades per bar | 0.2166 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-03_breakouts-pay-in-uptrends_1d_oos2`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
