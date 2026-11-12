---
backtest: 001-03_rsi-high-extreme-continuation-up_1h
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1h bars; fold A
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.602 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.667 | above 0 | no |
| Mean daily return | -0.002313 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.082 | above 0 | no |
| Calmar | -0.724 | above 0.75 | no |
| Trades per bar | 0.2172 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hourly_run/backtests/001-03_rsi-high-extreme-continuation-up_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
