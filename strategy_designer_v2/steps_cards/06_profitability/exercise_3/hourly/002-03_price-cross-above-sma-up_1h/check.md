---
backtest: 002-03_price-cross-above-sma-up_1h
data: BTC/USDT as BTCUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7287 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5493 | above 0 | yes |
| Mean daily return | 0.0009032 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1137 | above 0 | yes |
| Calmar | 0.6265 | above 0.75 | no |
| Trades per bar | 0.07535 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/hourly_run/backtests/002-03_price-cross-above-sma-up_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
