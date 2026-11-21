---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.048 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4667 | above 0 | yes |
| Mean daily return | 0.0007053 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8861 | above 0 | yes |
| Calmar | 1.08 | above 0.75 | yes |
| Trades per day | 0.1219 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold_paying_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
