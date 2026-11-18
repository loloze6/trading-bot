---
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.02401 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6155 | above 0 | no |
| Mean daily return | 4.012e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1006 | above 0 | no |
| Calmar | -0.004092 | above 0.75 | no |
| Trades per bar | 0.01951 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
