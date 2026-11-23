---
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5265 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.02769 | above 0 | no |
| Mean daily return | 5.48e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3782 | above 0 | yes |
| Calmar | 0.2179 | above 0.75 | no |
| Trades per day | 0.00485 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per day
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
