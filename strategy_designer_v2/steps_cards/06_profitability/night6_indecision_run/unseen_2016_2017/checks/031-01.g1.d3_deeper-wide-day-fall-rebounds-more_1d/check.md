---
backtest: 031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.392 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.359 | above 0 | no |
| Mean daily return, on days in a position | 0.007964 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.169 | above 0 | yes |
| Calmar | 2.853 | above 0.75 | yes |
| Trades per day | 0.02462 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.546 % |
| Yearly return | +15.0 % (over 1.99 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
