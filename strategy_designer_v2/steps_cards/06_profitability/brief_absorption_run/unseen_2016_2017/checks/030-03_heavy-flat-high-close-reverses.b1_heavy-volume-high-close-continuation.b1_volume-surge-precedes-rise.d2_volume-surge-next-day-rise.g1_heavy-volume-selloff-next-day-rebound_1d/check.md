---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.085 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.666 | above 0 | no |
| Mean daily return, on days in a position | 0.001936 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6632 | above 0 | yes |
| Calmar | 1.113 | above 0.75 | yes |
| Trades per day | 0.1508 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.997 % |
| Yearly return | +20.7 % (over 1.99 years) |
| Days in a position | 29 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/brief_absorption_run/unseen_2016_2017/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
