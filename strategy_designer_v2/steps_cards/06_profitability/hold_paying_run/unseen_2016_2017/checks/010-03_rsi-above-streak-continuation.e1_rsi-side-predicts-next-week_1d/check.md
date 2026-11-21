---
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.687 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.027 | above 0 | no |
| Mean daily return | 0.003217 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.085 | above 0 | yes |
| Calmar | 5.594 | above 0.75 | yes |
| Trades per day | 0.2483 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/hold_paying_run/unseen_2016_2017/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
