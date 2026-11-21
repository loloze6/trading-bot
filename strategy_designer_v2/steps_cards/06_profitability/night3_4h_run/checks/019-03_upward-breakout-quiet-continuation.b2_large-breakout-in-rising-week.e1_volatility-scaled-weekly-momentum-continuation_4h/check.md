---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4109 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1428 | above 0 | no |
| Mean daily return | 0.0004477 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2467 | above 0 | yes |
| Calmar | 0.1444 | above 0.75 | no |
| Trades per day | 1.268 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
