---
backtest: N2-04_slow-and-fast-momentum_1d_oos2
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds B, C
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.547 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.01775 | above 0 | no |
| Mean daily return | 0.004022 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8039 | above 0 | yes |
| Calmar | 2.944 | above 0.75 | yes |
| Trades per bar | 0.176 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N2-04_slow-and-fast-momentum_1d_oos2`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
