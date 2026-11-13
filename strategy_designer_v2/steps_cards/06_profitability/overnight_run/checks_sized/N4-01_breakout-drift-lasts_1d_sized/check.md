---
backtest: N4-01_breakout-drift-lasts_1d_sized
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8274 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2732 | above 0 | yes |
| Mean daily return | 0.0008634 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.677 | above 0 | yes |
| Calmar | 0.528 | above 0.75 | no |
| Trades per bar | 0.1594 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_sized/N4-01_breakout-drift-lasts_1d_sized`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
