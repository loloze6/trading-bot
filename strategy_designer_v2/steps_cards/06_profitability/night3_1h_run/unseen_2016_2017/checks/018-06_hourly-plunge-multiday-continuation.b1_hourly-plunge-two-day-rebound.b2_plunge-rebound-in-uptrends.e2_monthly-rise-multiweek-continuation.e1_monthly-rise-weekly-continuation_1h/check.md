---
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.162 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.07224 | above 0 | no |
| Mean daily return | 0.003597 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.76 | above 0 | yes |
| Calmar | 9.235 | above 0.75 | yes |
| Trades per day | 0.3014 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
