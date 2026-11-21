---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.185 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5662 | above 0 | no |
| Mean daily return | 0.003676 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.888 | above 0 | yes |
| Calmar | 11 | above 0.75 | yes |
| Trades per day | 0.1997 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/hold_paying_run/unseen_2016_2017/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
