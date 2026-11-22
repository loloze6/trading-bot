---
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4877 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1485 | above 0 | no |
| Mean daily return | 0.0009494 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3605 | above 0 | yes |
| Calmar | 0.1136 | above 0.75 | no |
| Trades per day | 0.9938 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
