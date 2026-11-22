---
backtest: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.166 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3881 | above 0 | no |
| Mean daily return | 1.982e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.03514 | above 0 | no |
| Calmar | 0.07007 | above 0.75 | no |
| Trades per day | 0.007019 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
