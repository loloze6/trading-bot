---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.042 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.488 | above 0 | yes |
| Mean daily return | 0.0008441 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8545 | above 0 | yes |
| Calmar | 1.14 | above 0.75 | yes |
| Trades per day | 0.1501 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
