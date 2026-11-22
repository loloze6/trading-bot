---
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5782 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05794 | above 0 | no |
| Mean daily return | 0.001035 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4411 | above 0 | yes |
| Calmar | 0.2489 | above 0.75 | no |
| Trades per day | 1.126 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
