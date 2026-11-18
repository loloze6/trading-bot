---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4547 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3567 | above 0 | yes |
| Mean daily return | 0.0003404 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6298 | above 0 | no |
| Calmar | 0.3767 | above 0.75 | no |
| Trades per bar | 0.3411 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
