---
backtest: N5-03_high-in-confirmed-uptrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6575 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.09843 | above 0 | yes |
| Mean daily return | 0.0008828 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3913 | above 0 | yes |
| Calmar | 0.3772 | above 0.1653 | yes |
| Trades per bar | 0.126 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests/N5-03_high-in-confirmed-uptrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
