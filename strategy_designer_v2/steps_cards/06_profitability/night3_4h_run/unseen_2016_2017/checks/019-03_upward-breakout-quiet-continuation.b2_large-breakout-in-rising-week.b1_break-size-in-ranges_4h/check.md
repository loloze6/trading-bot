---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.143 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.695 | above 0 | no |
| Mean daily return | 0.003591 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.608 | above 0 | yes |
| Calmar | 10.59 | above 0.75 | yes |
| Trades per day | 0.1994 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_4h_run/unseen_2016_2017/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
