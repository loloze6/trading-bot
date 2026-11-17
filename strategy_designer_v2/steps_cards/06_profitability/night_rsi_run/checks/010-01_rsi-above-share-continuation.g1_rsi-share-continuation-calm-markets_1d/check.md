---
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6085 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03103 | above 0 | no |
| Mean daily return | 0.0005091 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5062 | above 0 | yes |
| Calmar | 0.3365 | above 0.75 | no |
| Trades per bar | 0.1203 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
