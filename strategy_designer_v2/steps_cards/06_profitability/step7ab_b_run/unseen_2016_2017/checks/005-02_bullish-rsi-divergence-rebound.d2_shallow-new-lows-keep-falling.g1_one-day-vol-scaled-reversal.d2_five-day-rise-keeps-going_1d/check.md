---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.115 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5998 | above 0 | no |
| Mean daily return | 0.003396 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.891 | above 0 | yes |
| Calmar | 10.87 | above 0.75 | yes |
| Trades per day | 0.3591 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2016_2017/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
