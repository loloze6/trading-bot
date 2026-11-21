---
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.921 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3132 | above 0 | no |
| Mean daily return | 0.00297 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.515 | above 0 | yes |
| Calmar | 7.667 | above 0.75 | yes |
| Trades per day | 0.4377 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
