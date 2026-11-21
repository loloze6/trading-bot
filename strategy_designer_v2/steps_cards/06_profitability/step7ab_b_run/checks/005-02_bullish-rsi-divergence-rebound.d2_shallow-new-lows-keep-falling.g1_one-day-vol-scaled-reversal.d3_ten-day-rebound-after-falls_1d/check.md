---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.432 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2076 | above 0 | no |
| Mean daily return | 0.0008634 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2787 | above 0 | yes |
| Calmar | 0.05371 | above 0.75 | no |
| Trades per day | 0.09346 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
