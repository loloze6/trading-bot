---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7876 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2339 | above 0 | yes |
| Mean daily return | 0.001048 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6208 | above 0 | yes |
| Calmar | 0.497 | above 0.75 | no |
| Trades per day | 0.1421 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
