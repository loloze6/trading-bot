---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9647 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.383 | above 0 | yes |
| Mean daily return | 0.0003612 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.8345 | above 0 | yes |
| Calmar | 0.9113 | above 0.75 | yes |
| Trades per bar | 0.222 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
