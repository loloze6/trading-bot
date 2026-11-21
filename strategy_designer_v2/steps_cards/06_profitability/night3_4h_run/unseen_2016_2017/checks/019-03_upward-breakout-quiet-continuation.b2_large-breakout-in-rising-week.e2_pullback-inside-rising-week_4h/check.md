---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.999 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.8393 | above 0 | no |
| Mean daily return | 0.003071 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.538 | above 0 | yes |
| Calmar | 6.44 | above 0.75 | yes |
| Trades per day | 0.5351 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_4h_run/unseen_2016_2017/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
