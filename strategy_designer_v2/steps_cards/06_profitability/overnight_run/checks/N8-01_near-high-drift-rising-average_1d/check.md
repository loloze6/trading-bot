---
backtest: N8-01_near-high-drift-rising-average_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9237 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3695 | above 0 | yes |
| Mean daily return | 0.00137 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7462 | above 0 | yes |
| Calmar | 0.6653 | above 0.75 | no |
| Trades per bar | 0.1437 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N8-01_near-high-drift-rising-average_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
