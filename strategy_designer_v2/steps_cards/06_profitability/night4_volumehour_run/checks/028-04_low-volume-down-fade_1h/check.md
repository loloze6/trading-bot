---
backtest: 028-04_low-volume-down-fade_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3412 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9774 | above 0 | no |
| Mean daily return | -0.0002497 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4548 | above 0 | no |
| Calmar | -0.1764 | above 0.75 | no |
| Trades per day | 2.173 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
