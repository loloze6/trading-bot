---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.404 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.347 | above 0 | no |
| Mean daily return, on days in a position | 0.002865 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.085 | above 0 | yes |
| Calmar | 3.659 | above 0.75 | yes |
| Trades per day | 0.2202 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.416 % |
| Yearly return | +84.7 % (over 1.99 years) |
| Days in a position | 62 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night_006_run/unseen_2016_2017/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
