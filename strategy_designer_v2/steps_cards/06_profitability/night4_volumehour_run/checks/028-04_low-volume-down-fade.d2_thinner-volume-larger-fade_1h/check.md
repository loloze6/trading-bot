---
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.005025 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6412 | above 0 | no |
| Mean daily return | -7.339e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1446 | above 0 | no |
| Calmar | -0.1626 | above 0.75 | no |
| Trades per day | 5.394 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
