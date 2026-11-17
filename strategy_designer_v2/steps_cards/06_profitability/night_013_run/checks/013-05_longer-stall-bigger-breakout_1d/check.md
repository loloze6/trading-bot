---
backtest: 013-05_longer-stall-bigger-breakout_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.086 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5289 | above 0 | yes |
| Mean daily return | 0.0002319 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.9159 | above 0 | yes |
| Calmar | 1.16 | above 0.75 | yes |
| Trades per bar | 0.01214 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night_013_run/backtests/013-05_longer-stall-bigger-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
