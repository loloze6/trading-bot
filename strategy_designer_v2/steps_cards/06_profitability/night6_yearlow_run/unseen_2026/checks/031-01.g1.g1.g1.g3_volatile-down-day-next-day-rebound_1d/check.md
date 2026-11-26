---
backtest: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1653 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.06723 | above 0 | yes |
| Mean daily return, on days in a position | 0.0002625 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4378 | above 0 | no |
| Calmar | 0.2094 | above 0.75 | no |
| Trades per day | 0.05504 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.641 % |
| Yearly return | +1.3 % (over 0.87 years) |
| Days in a position | 21 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2026/backtests/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
