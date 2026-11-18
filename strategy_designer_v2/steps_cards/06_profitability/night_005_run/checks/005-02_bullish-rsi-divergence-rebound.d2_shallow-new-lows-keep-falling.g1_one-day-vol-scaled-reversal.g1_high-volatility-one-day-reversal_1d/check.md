---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2573 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3822 | above 0 | no |
| Mean daily return | 0.0001206 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.08635 | above 0 | yes |
| Calmar | 0.1421 | above 0.75 | no |
| Trades per bar | 0.6611 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
