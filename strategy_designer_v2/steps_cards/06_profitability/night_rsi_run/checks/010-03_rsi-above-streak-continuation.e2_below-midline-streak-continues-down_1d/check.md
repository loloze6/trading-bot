---
backtest: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.01853 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.621 | above 0 | no |
| Mean daily return | 1.416e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2326 | above 0 | no |
| Calmar | -0.05278 | above 0.75 | no |
| Trades per bar | 0.0938 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
