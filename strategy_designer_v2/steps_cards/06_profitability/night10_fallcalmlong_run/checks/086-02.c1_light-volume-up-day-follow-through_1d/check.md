---
backtest: 086-02.c1_light-volume-up-day-follow-through_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.446 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03876 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006405 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.317 | above 0 | yes |
| Calmar | 0.164 | above 0.75 | no |
| Trades per day | 0.05826 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.528 % |
| Yearly return | +4.1 % (over 8.6 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-02.c1_light-volume-up-day-follow-through_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
