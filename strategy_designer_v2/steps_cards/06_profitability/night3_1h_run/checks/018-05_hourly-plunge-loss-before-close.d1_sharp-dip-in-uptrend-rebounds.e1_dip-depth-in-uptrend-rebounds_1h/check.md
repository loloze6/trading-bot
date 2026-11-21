---
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.958 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4043 | above 0 | yes |
| Mean daily return | 0.0009507 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7755 | above 0 | yes |
| Calmar | 0.9269 | above 0.75 | yes |
| Trades per day | 0.3674 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
