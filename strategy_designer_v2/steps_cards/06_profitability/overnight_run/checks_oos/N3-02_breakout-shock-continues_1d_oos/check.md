---
backtest: N3-02_breakout-shock-continues_1d_oos
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6744 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3381 | above 0 | yes |
| Mean daily return | 0.000509 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3288 | above 0 | yes |
| Calmar | 0.5536 | above 0.75 | no |
| Trades per bar | 0.08282 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N3-02_breakout-shock-continues_1d_oos`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
