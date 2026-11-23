---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1779 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07982 | above 0 | yes |
| Mean daily return, on days in a position | 0.0001564 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3475 | above 0 | no |
| Calmar | 0.2621 | above 0.75 | no |
| Trades per day | 0.04206 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.482 % |
| Yearly return | +1.2 % (over 0.87 years) |
| Days in a position | 29 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/unseen_2026/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
