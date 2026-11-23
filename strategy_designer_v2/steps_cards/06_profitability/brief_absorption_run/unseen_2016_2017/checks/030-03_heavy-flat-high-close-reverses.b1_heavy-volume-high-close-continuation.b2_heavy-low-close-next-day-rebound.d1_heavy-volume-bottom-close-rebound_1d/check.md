---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6824 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.069 | above 0 | no |
| Mean daily return, on days in a position | 0.0007748 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2828 | above 0 | yes |
| Calmar | 0.74 | above 0.75 | no |
| Trades per day | 0.0619 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.476 % |
| Yearly return | +6.0 % (over 1.99 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/unseen_2016_2017/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
