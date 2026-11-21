---
backtest: 018-02_hourly-breakout-multiday-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.963 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2719 | above 0 | no |
| Mean daily return | 0.003298 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.667 | above 0 | yes |
| Calmar | 8.865 | above 0.75 | yes |
| Trades per day | 0.08538 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-02_hourly-breakout-multiday-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
