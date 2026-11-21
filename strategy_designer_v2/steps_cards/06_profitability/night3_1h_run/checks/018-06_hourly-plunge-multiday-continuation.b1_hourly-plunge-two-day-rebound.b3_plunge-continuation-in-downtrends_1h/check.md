---
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3092 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8629 | above 0 | no |
| Mean daily return | -0.0003582 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.507 | above 0 | no |
| Calmar | -0.2189 | above 0.75 | no |
| Trades per day | 0.3565 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
