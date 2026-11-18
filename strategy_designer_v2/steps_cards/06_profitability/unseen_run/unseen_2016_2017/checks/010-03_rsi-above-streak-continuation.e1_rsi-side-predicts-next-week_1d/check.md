---
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.168 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5462 | above 0 | no |
| Mean daily return | 0.004016 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.814 | above 0 | yes |
| Calmar | 9.652 | above 0.75 | yes |
| Trades per bar | 0.4227 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
