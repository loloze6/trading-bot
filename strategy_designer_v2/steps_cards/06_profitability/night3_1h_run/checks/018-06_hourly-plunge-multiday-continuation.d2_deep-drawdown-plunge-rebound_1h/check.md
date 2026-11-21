---
backtest: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2412 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3125 | above 0 | no |
| Mean daily return | 0.0002417 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1052 | above 0 | yes |
| Calmar | 0.02965 | above 0.75 | no |
| Trades per day | 0.2332 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
