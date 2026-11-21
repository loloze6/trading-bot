---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.98 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.7716 | above 0 | no |
| Mean daily return | 0.003056 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.474 | above 0 | yes |
| Calmar | 7.905 | above 0.75 | yes |
| Trades per day | 0.4036 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/hold2_rerun/unseen_2016_2017/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
