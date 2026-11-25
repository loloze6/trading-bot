---
backtest: 048-01_scaled-up-week-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.117 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6343 | above 0 | no |
| Mean daily return, on days in a position | 0.004313 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.744 | above 0 | yes |
| Calmar | 10.3 | above 0.75 | yes |
| Trades per day | 0.3287 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.061 % |
| Yearly return | +216.3 % (over 1.99 years) |
| Days in a position | 78 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2016_2017/backtests/048-01_scaled-up-week-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
