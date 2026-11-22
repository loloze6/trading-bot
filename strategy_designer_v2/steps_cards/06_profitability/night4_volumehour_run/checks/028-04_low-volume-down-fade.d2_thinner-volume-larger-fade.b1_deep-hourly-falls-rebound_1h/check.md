---
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7814 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.418 | above 0 | no |
| Mean daily return | -0.001031 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9342 | above 0 | no |
| Calmar | -0.3989 | above 0.75 | no |
| Trades per day | 8.442 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
