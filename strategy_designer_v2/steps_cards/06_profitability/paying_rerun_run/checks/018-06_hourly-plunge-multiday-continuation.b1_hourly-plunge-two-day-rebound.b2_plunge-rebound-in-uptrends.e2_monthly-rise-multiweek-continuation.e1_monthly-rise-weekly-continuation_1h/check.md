---
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.139 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5848 | above 0 | yes |
| Mean daily return | 0.001088 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9663 | above 0 | yes |
| Calmar | 1.055 | above 0.75 | yes |
| Trades per day | 0.2433 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
