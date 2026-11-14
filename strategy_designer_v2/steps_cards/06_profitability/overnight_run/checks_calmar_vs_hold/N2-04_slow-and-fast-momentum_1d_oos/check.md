---
backtest: N2-04_slow-and-fast-momentum_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.008 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6713 | above 0 | yes |
| Mean daily return | 0.001354 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5195 | above 0 | yes |
| Calmar | 1.148 | above -0.04838 | yes |
| Trades per bar | 0.1358 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N2-04_slow-and-fast-momentum_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
