---
backtest: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.183 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6552 | above 0 | no |
| Mean daily return | 0.004299 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.693 | above 0 | yes |
| Calmar | 10.47 | above 0.75 | yes |
| Trades per day | 0.193 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
