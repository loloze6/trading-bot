---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9453 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3911 | above 0 | yes |
| Mean daily return | 0.0006652 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8051 | above 0 | yes |
| Calmar | 0.8456 | above 0.75 | yes |
| Trades per day | 0.3171 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
