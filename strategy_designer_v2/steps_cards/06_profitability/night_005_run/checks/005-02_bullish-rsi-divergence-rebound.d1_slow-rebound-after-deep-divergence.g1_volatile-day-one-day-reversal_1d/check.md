---
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4862 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1534 | above 0 | no |
| Mean daily return | 0.0003832 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3208 | above 0 | yes |
| Calmar | 0.3026 | above 0.75 | no |
| Trades per bar | 0.3958 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
