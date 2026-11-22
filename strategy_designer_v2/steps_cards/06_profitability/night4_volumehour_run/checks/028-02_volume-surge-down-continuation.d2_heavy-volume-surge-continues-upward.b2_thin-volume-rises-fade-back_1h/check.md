---
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.931 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.568 | above 0 | no |
| Mean daily return | -0.001048 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.102 | above 0 | no |
| Calmar | -0.3446 | above 0.75 | no |
| Trades per day | 3.322 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
