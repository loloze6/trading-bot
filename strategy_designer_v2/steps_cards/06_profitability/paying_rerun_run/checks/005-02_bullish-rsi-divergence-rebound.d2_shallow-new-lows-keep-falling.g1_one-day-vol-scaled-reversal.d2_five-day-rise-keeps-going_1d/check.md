---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.211 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5716 | above 0 | yes |
| Mean daily return | 0.0011 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.086 | above 0 | yes |
| Calmar | 1.307 | above 0.75 | yes |
| Trades per day | 0.3293 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
