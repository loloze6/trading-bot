---
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9924 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3529 | above 0 | yes |
| Mean daily return | 0.001078 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8652 | above 0 | yes |
| Calmar | 0.8976 | above 0.75 | yes |
| Trades per day | 0.2479 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold_paying_run/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
