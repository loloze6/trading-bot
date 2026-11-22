---
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.579 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.215 | above 0 | no |
| Mean daily return | -0.001292 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.721 | above 0 | no |
| Calmar | -0.4083 | above 0.75 | no |
| Trades per day | 2.74 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
