---
backtest: N4-04_dip-rebound-spans-days_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1191 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2173 | above 0 | no |
| Mean daily return | 7.615e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1486 | above 0 | no |
| Calmar | 0.001789 | above -0.04838 | yes |
| Trades per bar | 0.07998 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-04_dip-rebound-spans-days_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
