---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4609 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.176 | above 0 | no |
| Mean daily return | -0.0003581 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.844 | above 0 | no |
| Calmar | -0.367 | above 0.75 | no |
| Trades per bar | 0.1669 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
