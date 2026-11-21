---
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8831 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3294 | above 0 | yes |
| Mean daily return | 0.00112 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7121 | above 0 | yes |
| Calmar | 0.6024 | above 0.75 | no |
| Trades per day | 0.2765 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
