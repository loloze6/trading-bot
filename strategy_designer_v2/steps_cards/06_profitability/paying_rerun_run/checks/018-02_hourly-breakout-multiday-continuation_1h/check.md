---
backtest: 018-02_hourly-breakout-multiday-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.086 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.532 | above 0 | yes |
| Mean daily return | 0.0008354 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9521 | above 0 | yes |
| Calmar | 1.099 | above 0.75 | yes |
| Trades per day | 0.06739 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/018-02_hourly-breakout-multiday-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
