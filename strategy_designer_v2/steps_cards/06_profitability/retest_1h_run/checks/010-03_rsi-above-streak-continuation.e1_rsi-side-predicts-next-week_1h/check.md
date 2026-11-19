---
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.504 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.14 | above 0 | no |
| Mean daily return | -0.002095 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.885 | above 0 | no |
| Calmar | -0.5886 | above 0.75 | no |
| Trades per day | 12.11 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
