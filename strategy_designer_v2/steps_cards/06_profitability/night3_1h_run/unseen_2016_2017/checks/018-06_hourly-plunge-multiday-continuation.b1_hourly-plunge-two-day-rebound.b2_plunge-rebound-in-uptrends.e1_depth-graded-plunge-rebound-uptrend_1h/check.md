---
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.977 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2578 | above 0 | no |
| Mean daily return | 0.004119 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.511 | above 0 | yes |
| Calmar | 9.469 | above 0.75 | yes |
| Trades per day | 0.1371 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
