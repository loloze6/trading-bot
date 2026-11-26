---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4631 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.288 | above 0 | no |
| Mean daily return, on days in a position | 0.002075 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1447 | above 0 | yes |
| Calmar | 0.4213 | above 0.75 | no |
| Trades per day | 0.01368 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.228 % |
| Yearly return | +1.9 % (over 1.99 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/step3_situation_run/unseen_2016_2017/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
