---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4409 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1986 | above 0 | no |
| Mean daily return | 0.0003298 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3017 | above 0 | yes |
| Calmar | 0.2134 | above 0.75 | no |
| Trades per day | 0.1337 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/hold2_rerun/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
