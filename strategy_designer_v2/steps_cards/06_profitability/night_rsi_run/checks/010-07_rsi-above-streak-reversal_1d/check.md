---
backtest: 010-07_rsi-above-streak-reversal_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.102 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.741 | above 0 | no |
| Mean daily return | -0.0009731 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.167 | above 0 | no |
| Calmar | -0.3449 | above 0.75 | no |
| Trades per bar | 0.09706 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-07_rsi-above-streak-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
