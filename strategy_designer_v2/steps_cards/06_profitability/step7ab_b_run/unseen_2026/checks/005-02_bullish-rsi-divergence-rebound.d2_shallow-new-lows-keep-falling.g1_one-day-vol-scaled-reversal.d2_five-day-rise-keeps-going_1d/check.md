---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.005226 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6271 | above 0 | yes |
| Mean daily return | 4.761e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.015 | above 0 | no |
| Calmar | -0.2185 | above 0.75 | no |
| Trades per day | 0.2897 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2026/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
