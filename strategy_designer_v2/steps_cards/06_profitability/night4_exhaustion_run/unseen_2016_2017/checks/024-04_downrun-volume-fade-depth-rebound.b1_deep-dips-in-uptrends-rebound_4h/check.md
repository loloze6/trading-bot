---
backtest: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.224 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6141 | above 0 | no |
| Mean daily return | 0.004524 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.697 | above 0 | yes |
| Calmar | 11.25 | above 0.75 | yes |
| Trades per day | 0.1252 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
