---
backtest: 050-04.b1_range-scaled-week-rise-more-coins_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5008 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.0936 | above 0 | yes |
| Mean daily return, on days in a position | 0.001099 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3053 | above 0 | yes |
| Calmar | 0.2361 | above 0.75 | no |
| Trades per day | 0.0598 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.502 % |
| Yearly return | +4.4 % (over 8.6 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-04.b1_range-scaled-week-rise-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
