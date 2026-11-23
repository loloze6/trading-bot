---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7954 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2412 | above 0 | yes |
| Mean daily return, on days in a position | 0.001174 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6252 | above 0 | yes |
| Calmar | 0.6469 | above 0.75 | no |
| Trades per day | 0.3217 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.482 % |
| Yearly return | +20.3 % (over 7.94 years) |
| Days in a position | 53 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
