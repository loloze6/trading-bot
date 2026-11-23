---
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.533 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.248 | above 0 | no |
| Mean daily return, on days in a position | 0.002025 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.141 | above 0 | yes |
| Calmar | 2.323 | above 0.75 | yes |
| Trades per day | 0.1708 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.114 % |
| Yearly return | +35.4 % (over 1.99 years) |
| Days in a position | 44 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night_run/unseen_2016_2017/backtests/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
