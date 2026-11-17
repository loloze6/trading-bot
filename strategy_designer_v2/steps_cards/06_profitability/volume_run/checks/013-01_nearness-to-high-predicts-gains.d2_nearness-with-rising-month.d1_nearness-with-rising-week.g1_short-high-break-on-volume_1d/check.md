---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6037 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.04949 | above 0 | yes |
| Mean daily return | 0.00023 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4289 | above 0 | yes |
| Calmar | 0.3868 | above 0.75 | no |
| Trades per bar | 0.442 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/volume_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
