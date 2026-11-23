---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7375 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1833 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009774 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5952 | above 0 | yes |
| Calmar | 0.5775 | above 0.75 | no |
| Trades per day | 0.3711 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.774 % |
| Yearly return | +21.1 % (over 7.94 years) |
| Days in a position | 70 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
