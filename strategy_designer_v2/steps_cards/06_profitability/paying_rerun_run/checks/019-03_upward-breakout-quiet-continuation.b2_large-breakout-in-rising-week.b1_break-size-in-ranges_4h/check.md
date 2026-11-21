---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.112 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5582 | above 0 | yes |
| Mean daily return | 0.001115 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9789 | above 0 | yes |
| Calmar | 1.211 | above 0.75 | yes |
| Trades per day | 0.2147 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
