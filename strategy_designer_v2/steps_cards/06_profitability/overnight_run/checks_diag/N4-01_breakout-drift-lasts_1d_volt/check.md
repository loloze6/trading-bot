---
backtest: N4-01_breakout-drift-lasts_1d_volt
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7522 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.198 | above 0 | yes |
| Mean daily return | 0.001232 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5848 | above 0 | yes |
| Calmar | 0.4043 | above 0.75 | no |
| Trades per bar | 0.1289 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_diag/N4-01_breakout-drift-lasts_1d_volt`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
