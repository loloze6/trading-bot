---
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8447 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.291 | above 0 | yes |
| Mean daily return | 0.0004962 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6381 | above 0 | yes |
| Calmar | 0.7128 | above 0.75 | no |
| Trades per day | 0.252 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
