---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9635 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4093 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009065 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8901 | above 0 | yes |
| Calmar | 1.178 | above 0.75 | yes |
| Trades per day | 0.0525 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.430 % |
| Yearly return | +7.9 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
