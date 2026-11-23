---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8045 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2503 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008772 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6617 | above 0 | yes |
| Calmar | 0.7677 | above 0.75 | yes |
| Trades per day | 0.4152 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.537 % |
| Yearly return | +21.2 % (over 7.94 years) |
| Days in a position | 74 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
