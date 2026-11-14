---
backtest: N3-02_breakout-shock-continues_1d_oos2
data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds B, C
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7325 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.9121 | above 0 | no |
| Mean daily return | 0.001359 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1641 | above 0 | yes |
| Calmar | 0.6079 | above 0.75 | no |
| Trades per bar | 0.1045 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N3-02_breakout-shock-continues_1d_oos2`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
