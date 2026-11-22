---
backtest: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4735 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.11 | above 0 | no |
| Mean daily return | -0.0005809 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6173 | above 0 | no |
| Calmar | -0.2958 | above 0.75 | no |
| Trades per day | 4.264 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
