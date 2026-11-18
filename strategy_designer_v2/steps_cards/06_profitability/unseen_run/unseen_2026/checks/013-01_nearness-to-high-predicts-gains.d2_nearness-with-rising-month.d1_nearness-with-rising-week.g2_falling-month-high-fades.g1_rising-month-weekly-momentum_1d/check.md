---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7384 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6403 | above 0 | yes |
| Mean daily return | 0.0004564 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.0555 | above 0 | no |
| Calmar | 0.9724 | above 0.75 | yes |
| Trades per bar | 0.1895 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
