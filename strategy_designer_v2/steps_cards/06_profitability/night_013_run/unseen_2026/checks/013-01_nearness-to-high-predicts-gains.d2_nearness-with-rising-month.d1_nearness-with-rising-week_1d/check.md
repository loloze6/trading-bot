---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.579 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.481 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006772 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.537 | above 0 | yes |
| Calmar | 4.275 | above 0.75 | yes |
| Trades per day | 0.2279 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.487 % |
| Yearly return | +15.3 % (over 0.87 years) |
| Days in a position | 59 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night_013_run/unseen_2026/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
