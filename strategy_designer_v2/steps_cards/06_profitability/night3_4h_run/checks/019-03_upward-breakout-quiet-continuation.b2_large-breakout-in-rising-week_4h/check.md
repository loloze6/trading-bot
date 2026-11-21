---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.088 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5343 | above 0 | yes |
| Mean daily return | 0.001099 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9532 | above 0 | yes |
| Calmar | 1.174 | above 0.75 | yes |
| Trades per day | 0.2208 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
