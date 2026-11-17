---
backtest: 010-08_rsi-below-streak-reversal_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.09255 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7321 | above 0 | no |
| Mean daily return | -7.242e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1365 | above 0 | no |
| Calmar | -0.1149 | above 0.75 | no |
| Trades per bar | 0.08901 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-08_rsi-below-streak-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
