---
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1323 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7685 | above 0 | no |
| Mean daily return | -0.0001606 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2647 | above 0 | no |
| Calmar | -0.1821 | above 0.75 | no |
| Trades per day | 2.877 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.d2_volume-surge-rises-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
