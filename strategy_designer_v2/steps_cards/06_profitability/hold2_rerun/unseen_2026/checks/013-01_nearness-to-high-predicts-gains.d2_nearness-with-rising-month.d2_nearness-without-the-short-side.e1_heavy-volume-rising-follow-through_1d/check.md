---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6663 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5683 | above 0 | yes |
| Mean daily return | 0.0005497 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.2344 | above 0 | no |
| Calmar | 0.6946 | above 0.75 | no |
| Trades per day | 0.3531 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold2_rerun/unseen_2026/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
