---
backtest: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.565 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.522 | above 0 | no |
| Mean daily return | 0.001058 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8641 | above 0 | yes |
| Calmar | 2.119 | above 0.75 | yes |
| Trades per day | 1.655 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_volumehour_run/unseen_2016_2017/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
