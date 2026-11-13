---
backtest: N4-01_breakout-drift-lasts_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7897 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2355 | above 0 | yes |
| Mean daily return | 0.0004327 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5928 | above 0 | yes |
| Calmar | 0.4865 | above 0.75 | no |
| Trades per bar | 0.1734 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-01_breakout-drift-lasts_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
