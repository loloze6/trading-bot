---
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.194 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.83 | above 0 | no |
| Mean daily return | -0.001119 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.353 | above 0 | no |
| Calmar | -0.3834 | above 0.75 | no |
| Trades per day | 4.409 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
