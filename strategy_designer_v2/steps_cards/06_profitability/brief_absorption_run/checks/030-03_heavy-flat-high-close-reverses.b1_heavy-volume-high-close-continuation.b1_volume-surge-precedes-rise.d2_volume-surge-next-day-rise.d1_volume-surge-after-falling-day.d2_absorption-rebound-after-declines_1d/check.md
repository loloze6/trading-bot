---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4934 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06077 | above 0 | no |
| Mean daily return, on days in a position | 0.0009664 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4273 | above 0 | yes |
| Calmar | 0.2188 | above 0.75 | no |
| Trades per day | 0.1658 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.335 % |
| Yearly return | +9.7 % (over 7.94 years) |
| Days in a position | 36 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
