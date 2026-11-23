---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.068 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.166 | above 0 | no |
| Mean daily return, on days in a position | -0.002224 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.353 | above 0 | no |
| Calmar | -0.9608 | above 0.75 | no |
| Trades per day | 0.1771 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.372 % |
| Yearly return | -27.0 % (over 0.87 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/unseen_2026/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
