---
backtest: N6-01_breakout-after-longer-decline_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.385 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1692 | above 0 | no |
| Mean daily return | 0.00012 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1663 | above 0 | yes |
| Calmar | 0.1183 | above 0.75 | no |
| Trades per bar | 0.05792 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N6-01_breakout-after-longer-decline_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
