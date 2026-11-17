---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.006 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4246 | above 0 | yes |
| Mean daily return | 0.0006353 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8402 | above 0 | yes |
| Calmar | 0.9636 | above 0.75 | yes |
| Trades per bar | 0.1386 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
