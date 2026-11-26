---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.51 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4119 | above 0 | yes |
| Mean daily return, on days in a position | 0.002529 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -1.152 | above 0 | no |
| Calmar | 0.8483 | above 0.75 | yes |
| Trades per day | 0.0161 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.305 % |
| Yearly return | +2.8 % (over 0.87 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/step3_situation_run/unseen_2026/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
