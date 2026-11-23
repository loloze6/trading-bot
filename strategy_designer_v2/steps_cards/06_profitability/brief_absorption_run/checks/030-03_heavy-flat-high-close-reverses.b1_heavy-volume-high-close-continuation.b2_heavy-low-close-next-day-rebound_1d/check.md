---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8321 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2779 | above 0 | yes |
| Mean daily return, on days in a position | 0.00185 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7225 | above 0 | yes |
| Calmar | 0.6738 | above 0.75 | no |
| Trades per day | 0.08075 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.645 % |
| Yearly return | +10.0 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
