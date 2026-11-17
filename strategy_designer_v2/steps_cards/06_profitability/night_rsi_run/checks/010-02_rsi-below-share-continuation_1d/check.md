---
backtest: 010-02_rsi-below-share-continuation_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8297 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1901 | above 0 | yes |
| Mean daily return | 0.0009919 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6977 | above 0 | yes |
| Calmar | 0.5774 | above 0.75 | no |
| Trades per bar | 0.1642 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-02_rsi-below-share-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
