---
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.502 | above 0 | yes |
| Sharpe minus holding's Sharpe | 2.124 | above 0 | yes |
| Mean daily return | 0.002317 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.142 | above 0 | yes |
| Calmar | 3.994 | above 0.75 | yes |
| Trades per day | 0.4143 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold2_rerun_run/unseen_2026/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
