---
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.839 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.912 | above 0 | no |
| Mean daily return, on days in a position | 0.0006941 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.492 | above 0 | yes |
| Calmar | 3.871 | above 0.75 | yes |
| Trades per day | 0.2137 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.718 % |
| Yearly return | +27.5 % (over 1.99 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night_013_run/unseen_2016_2017/backtests/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
