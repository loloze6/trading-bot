---
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7197 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.356 | above 0 | no |
| Mean daily return | -0.0006118 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8162 | above 0 | no |
| Calmar | -0.2618 | above 0.75 | no |
| Trades per day | 2.663 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
