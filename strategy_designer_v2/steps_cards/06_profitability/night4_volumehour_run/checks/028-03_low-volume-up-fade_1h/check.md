---
backtest: 028-03_low-volume-up-fade_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.633 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.269 | above 0 | no |
| Mean daily return | -0.001822 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.783 | above 0 | no |
| Calmar | -0.5283 | above 0.75 | no |
| Trades per day | 3.412 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
