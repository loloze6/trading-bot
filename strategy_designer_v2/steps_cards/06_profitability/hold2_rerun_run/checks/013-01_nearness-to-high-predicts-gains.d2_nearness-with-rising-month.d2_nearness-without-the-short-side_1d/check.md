---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.049 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.467 | above 0 | yes |
| Mean daily return | 0.0006998 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8849 | above 0 | yes |
| Calmar | 1.042 | above 0.75 | yes |
| Trades per day | 0.1226 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold2_rerun_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
