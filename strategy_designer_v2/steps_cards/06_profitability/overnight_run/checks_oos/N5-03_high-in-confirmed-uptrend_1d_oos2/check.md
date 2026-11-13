---
backtest: N5-03_high-in-confirmed-uptrend_1d_oos2
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds B, C
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.353 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2193 | above 0 | no |
| Mean daily return | 0.00377 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4814 | above 0 | yes |
| Calmar | 1.826 | above 0.75 | yes |
| Trades per bar | 0.1853 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N5-03_high-in-confirmed-uptrend_1d_oos2`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
