---
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.9338 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.488 | above 0 | no |
| Mean daily return | -0.000391 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.059 | above 0 | no |
| Calmar | -0.2006 | above 0.75 | no |
| Trades per day | 1.666 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
