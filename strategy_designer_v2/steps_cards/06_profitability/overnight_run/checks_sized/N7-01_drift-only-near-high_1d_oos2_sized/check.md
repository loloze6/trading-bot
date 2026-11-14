---
backtest: N7-01_drift-only-near-high_1d_oos2_sized
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds B, C
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.733 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.212 | above 0 | yes |
| Mean daily return | 0.001779 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.163 | above 0 | yes |
| Calmar | 2.263 | above 0.75 | yes |
| Trades per bar | 0.1882 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_sized/N7-01_drift-only-near-high_1d_oos2_sized`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
