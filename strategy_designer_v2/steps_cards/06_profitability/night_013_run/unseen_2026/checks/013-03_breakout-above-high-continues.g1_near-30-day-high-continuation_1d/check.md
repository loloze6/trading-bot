---
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.697 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.599 | above 0 | yes |
| Mean daily return, on days in a position | 0.0005405 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5486 | above 0 | yes |
| Calmar | 4.484 | above 0.75 | yes |
| Trades per day | 0.1428 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.602 % |
| Yearly return | +20.8 % (over 0.87 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night_013_run/unseen_2026/backtests/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
