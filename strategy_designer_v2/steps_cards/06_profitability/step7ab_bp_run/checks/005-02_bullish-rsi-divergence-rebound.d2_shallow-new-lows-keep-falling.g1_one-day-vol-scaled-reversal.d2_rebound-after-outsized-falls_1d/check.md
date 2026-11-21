---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1511 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4884 | above 0 | no |
| Mean daily return | 0.0001108 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.04005 | above 0 | yes |
| Calmar | 0.009193 | above 0.75 | no |
| Trades per day | 0.2172 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
