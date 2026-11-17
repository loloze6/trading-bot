---
backtest: 013-06_breakout-volume-drives-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8323 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2627 | above 0 | yes |
| Mean daily return | 0.0001524 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6349 | above 0 | yes |
| Calmar | 0.727 | above 0.75 | no |
| Trades per bar | 0.01958 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/volume_run/backtests/013-06_breakout-volume-drives-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
