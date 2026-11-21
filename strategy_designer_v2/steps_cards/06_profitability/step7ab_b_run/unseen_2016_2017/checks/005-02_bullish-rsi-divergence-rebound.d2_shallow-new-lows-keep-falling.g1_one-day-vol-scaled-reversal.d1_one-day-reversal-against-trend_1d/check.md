---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1042 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.61 | above 0 | no |
| Mean daily return | 7.998e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4546 | above 0 | no |
| Calmar | -0.034 | above 0.75 | no |
| Trades per day | 0.3112 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2016_2017/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
