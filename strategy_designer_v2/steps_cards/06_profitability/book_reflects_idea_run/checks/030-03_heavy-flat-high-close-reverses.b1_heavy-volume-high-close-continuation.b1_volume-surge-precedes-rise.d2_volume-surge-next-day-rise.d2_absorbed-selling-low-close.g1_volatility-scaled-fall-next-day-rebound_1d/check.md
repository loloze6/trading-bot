---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2437 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3105 | above 0 | no |
| Mean daily return, on days in a position | 0.001038 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1288 | above 0 | yes |
| Calmar | 0.1065 | above 0.75 | no |
| Trades per day | 0.05404 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.924 % |
| Yearly return | +2.8 % (over 7.94 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/book_reflects_idea_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
