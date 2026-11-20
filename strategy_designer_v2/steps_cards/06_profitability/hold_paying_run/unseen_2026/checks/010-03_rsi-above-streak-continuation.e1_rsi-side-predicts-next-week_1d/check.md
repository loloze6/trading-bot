---
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1645 | above 0 | no |
| Sharpe minus holding's Sharpe | 0.4574 | above 0 | yes |
| Mean daily return | -0.0001479 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.634 | above 0 | no |
| Calmar | -0.3479 | above 0.75 | no |
| Trades per day | 0.2025 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_paying_run/unseen_2026/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
