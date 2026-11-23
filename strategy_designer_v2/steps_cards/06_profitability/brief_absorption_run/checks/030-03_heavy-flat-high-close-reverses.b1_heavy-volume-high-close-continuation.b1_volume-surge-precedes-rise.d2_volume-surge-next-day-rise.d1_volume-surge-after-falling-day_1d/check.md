---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.723 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1689 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007887 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5692 | above 0 | yes |
| Calmar | 0.6272 | above 0.75 | no |
| Trades per day | 0.3274 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.316 % |
| Yearly return | +16.1 % (over 7.94 years) |
| Days in a position | 63 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
