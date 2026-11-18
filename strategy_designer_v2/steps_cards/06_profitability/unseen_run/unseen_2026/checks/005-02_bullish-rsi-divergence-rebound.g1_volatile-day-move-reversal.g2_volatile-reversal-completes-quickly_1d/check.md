---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5812 | above 0 | no |
| Sharpe minus holding's Sharpe | 0.04069 | above 0 | yes |
| Mean daily return | -0.0005251 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.768 | above 0 | no |
| Calmar | -0.8553 | above 0.75 | no |
| Trades per bar | 0.1464 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
