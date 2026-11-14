---
backtest: N3-04_dip-in-uptrend_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.105 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2314 | above 0 | no |
| Mean daily return | 6.685e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1727 | above 0 | no |
| Calmar | -0.005352 | above 0.75 | no |
| Trades per bar | 0.09011 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N3-04_dip-in-uptrend_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
