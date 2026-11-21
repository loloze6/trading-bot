---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.09818 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7201 | above 0 | yes |
| Mean daily return | 7.495e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8065 | above 0 | no |
| Calmar | -0.05209 | above 0.75 | no |
| Trades per day | 0.3551 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2026/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
