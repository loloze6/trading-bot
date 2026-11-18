---
backtest: 012-01_liquidation-flush-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.03091 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5851 | above 0 | no |
| Mean daily return | -4.062e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1858 | above 0 | no |
| Calmar | -0.02097 | above 0.75 | no |
| Trades per bar | 0.00913 | at least 0.01 | no |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar; Trades per bar
Record: `steps_cards/04_backtest/night_012_run/backtests/012-01_liquidation-flush-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
