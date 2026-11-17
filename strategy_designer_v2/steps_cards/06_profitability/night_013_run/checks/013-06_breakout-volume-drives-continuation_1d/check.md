---
backtest: 013-06_breakout-volume-drives-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8329 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2633 | above 0 | yes |
| Mean daily return | 0.0001526 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6356 | above 0 | yes |
| Calmar | 0.7309 | above 0.75 | no |
| Trades per bar | 0.01946 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-06_breakout-volume-drives-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
