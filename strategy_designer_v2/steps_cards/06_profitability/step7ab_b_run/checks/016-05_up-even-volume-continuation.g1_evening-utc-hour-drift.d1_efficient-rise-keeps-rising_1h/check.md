---
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7528 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.199 | above 0 | yes |
| Mean daily return | 0.0009246 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5892 | above 0 | yes |
| Calmar | 0.5571 | above 0.75 | no |
| Trades per day | 0.7342 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
