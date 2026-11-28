---
backtest: 050-02.b2_calm-downtrend-week-rise-five-days_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4314 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.02421 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008874 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2482 | above 0 | yes |
| Calmar | 0.1577 | above 0.75 | no |
| Trades per day | 0.05647 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.582 % |
| Yearly return | +4.3 % (over 8.6 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b2_calm-downtrend-week-rise-five-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
