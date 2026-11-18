---
backtest: 012-04_flush-depth-retracement-size_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3106 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8647 | above 0 | no |
| Mean daily return | -5.06e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4178 | above 0 | no |
| Calmar | -0.1009 | above 0.75 | no |
| Trades per bar | 0.00428 | at least 0.01 | no |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar; Trades per bar
Record: `steps_cards/04_backtest/volume_run/backtests/012-04_flush-depth-retracement-size_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
