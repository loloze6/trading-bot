---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7213 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1675 | above 0 | yes |
| Mean daily return | 0.0003667 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5438 | above 0 | yes |
| Calmar | 0.514 | above 0.75 | no |
| Trades per day | 0.9164 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
