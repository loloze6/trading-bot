---
backtest: 058-03.e1_calm-rise-stretch-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.224 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.9653 | above 0 | no |
| Mean daily return, on days in a position | 0.006278 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.922 | above 0 | yes |
| Calmar | 3.324 | above 0.75 | yes |
| Trades per day | 0.05093 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.276 % |
| Yearly return | +66.9 % (over 1.99 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_2016_2017/backtests/058-03.e1_calm-rise-stretch-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
