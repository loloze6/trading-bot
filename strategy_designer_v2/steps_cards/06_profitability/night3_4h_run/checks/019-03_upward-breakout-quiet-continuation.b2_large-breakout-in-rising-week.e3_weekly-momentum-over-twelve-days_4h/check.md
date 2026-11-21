---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2682 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2855 | above 0 | no |
| Mean daily return | 0.0003328 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.08896 | above 0 | yes |
| Calmar | 0.023 | above 0.75 | no |
| Trades per day | 0.289 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
