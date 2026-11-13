---
backtest: N4-04_dip-rebound-spans-days_1d_oos2
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds B, C
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.826 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1684 | above 0 | yes |
| Mean daily return | 0.002217 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.58 | above 0 | yes |
| Calmar | 3.854 | above 0.75 | yes |
| Trades per bar | 0.1108 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-04_dip-rebound-spans-days_1d_oos2`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
