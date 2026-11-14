---
backtest: 002-01_sma-cross-up-drift-up_1h
data: BTC/USDT as BTCUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6358 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4564 | above 0 | yes |
| Mean daily return | 0.0007456 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.154 | above 0 | no |
| Calmar | 0.3814 | above 0.75 | no |
| Trades per bar | 0.0355 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hourly_run/backtests/002-01_sma-cross-up-drift-up_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
