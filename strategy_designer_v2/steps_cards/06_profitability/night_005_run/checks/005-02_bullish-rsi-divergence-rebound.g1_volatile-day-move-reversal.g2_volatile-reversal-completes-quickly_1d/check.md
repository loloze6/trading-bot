---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.155 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5158 | above 0 | yes |
| Mean daily return | 0.0006184 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.055 | above 0 | yes |
| Calmar | 1.047 | above 0.75 | yes |
| Trades per bar | 0.1599 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
