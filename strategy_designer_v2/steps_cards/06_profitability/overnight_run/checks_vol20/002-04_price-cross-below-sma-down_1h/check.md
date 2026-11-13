---
backtest: 002-04_price-cross-below-sma-down_1h
data: BTC/USDT as BTCUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1044 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.075 | above 0 | no |
| Mean daily return | 5.719e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5615 | above 0 | no |
| Calmar | 0.006465 | above 0.75 | no |
| Trades per bar | 0.09875 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hourly_run/backtests/002-04_price-cross-below-sma-down_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
