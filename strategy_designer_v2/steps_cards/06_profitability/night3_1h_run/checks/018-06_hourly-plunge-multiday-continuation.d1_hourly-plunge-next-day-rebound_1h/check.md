---
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.534 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.01973 | above 0 | no |
| Mean daily return | 0.0005107 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3954 | above 0 | yes |
| Calmar | 0.2482 | above 0.75 | no |
| Trades per day | 1.32 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
