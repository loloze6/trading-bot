---
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.063 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.161 | above 0 | no |
| Mean daily return, on days in a position | -0.001384 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.713 | above 0 | no |
| Calmar | -0.9717 | above 0.75 | no |
| Trades per day | 0.2399 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.482 % |
| Yearly return | -28.9 % (over 0.87 years) |
| Days in a position | 60 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_run/unseen_2026/backtests/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
