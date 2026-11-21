---
backtest: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8664 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3126 | above 0 | yes |
| Mean daily return | 0.0006972 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6948 | above 0 | yes |
| Calmar | 0.831 | above 0.75 | yes |
| Trades per day | 0.3898 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
