---
backtest: 001-04_rsi-low-extreme-continuation-down_1h
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.6 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.665 | above 0 | no |
| Mean daily return | -0.0008764 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.348 | above 0 | no |
| Calmar | -0.5423 | above 0.75 | no |
| Trades per bar | 0.1895 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hourly_run/backtests/001-04_rsi-low-extreme-continuation-down_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
