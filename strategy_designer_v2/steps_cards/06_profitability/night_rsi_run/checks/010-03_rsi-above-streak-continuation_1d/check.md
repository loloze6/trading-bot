---
backtest: 010-03_rsi-above-streak-continuation_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.04 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4007 | above 0 | yes |
| Mean daily return | 0.0009233 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.811 | above 0 | yes |
| Calmar | 0.9158 | above 0.75 | yes |
| Trades per bar | 0.08251 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-03_rsi-above-streak-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
