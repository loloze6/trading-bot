---
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6916 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1379 | above 0 | yes |
| Mean daily return | 0.000928 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.513 | above 0 | yes |
| Calmar | 0.4717 | above 0.75 | no |
| Trades per day | 0.2648 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
