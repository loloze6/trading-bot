---
backtest: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9822 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.346 | above 0 | yes |
| Mean daily return | 0.0007641 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8677 | above 0 | yes |
| Calmar | 0.968 | above 0.75 | yes |
| Trades per day | 1.362 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
