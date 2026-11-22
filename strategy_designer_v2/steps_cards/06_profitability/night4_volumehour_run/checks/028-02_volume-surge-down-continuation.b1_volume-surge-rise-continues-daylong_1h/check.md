---
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.596 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.04016 | above 0 | no |
| Mean daily return | 0.001153 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4604 | above 0 | yes |
| Calmar | 0.2496 | above 0.75 | no |
| Trades per day | 1.003 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
