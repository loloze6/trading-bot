---
backtest: 002-02_sma-cross-down-drift-down_1h
data: BTC/USDT as BTCUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4611 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2817 | above 0 | yes |
| Mean daily return | 0.0007919 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1328 | above 0 | no |
| Calmar | 0.2142 | above -0.07741 | yes |
| Trades per bar | 0.04127 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/hourly_run/backtests/002-02_sma-cross-down-drift-down_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
