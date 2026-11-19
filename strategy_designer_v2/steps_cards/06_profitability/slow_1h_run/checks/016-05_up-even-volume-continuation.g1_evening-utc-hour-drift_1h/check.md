---
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.868 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.422 | above 0 | no |
| Mean daily return | -0.0008396 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -3.001 | above 0 | no |
| Calmar | -0.2927 | above 0.75 | no |
| Trades per day | 0.9743 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
