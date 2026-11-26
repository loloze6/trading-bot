---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6727 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1185 | above 0 | yes |
| Mean daily return, on days in a position | 0.001921 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5169 | above 0 | yes |
| Calmar | 0.3995 | above 0.75 | no |
| Trades per day | 0.09821 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.209 % |
| Yearly return | +13.7 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/book_reflects_idea_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
