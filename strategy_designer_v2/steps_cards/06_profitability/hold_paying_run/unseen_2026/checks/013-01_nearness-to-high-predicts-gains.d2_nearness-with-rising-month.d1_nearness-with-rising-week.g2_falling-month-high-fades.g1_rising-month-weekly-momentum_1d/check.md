---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4916 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3935 | above 0 | yes |
| Mean daily return | 0.0003493 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3244 | above 0 | no |
| Calmar | 0.5491 | above 0.75 | no |
| Trades per day | 0.1506 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_paying_run/unseen_2026/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
