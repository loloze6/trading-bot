---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8146 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.175 | above 0 | yes |
| Mean daily return | 0.0006573 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7106 | above 0 | yes |
| Calmar | 0.7608 | above 0.75 | yes |
| Trades per day | 0.356 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
