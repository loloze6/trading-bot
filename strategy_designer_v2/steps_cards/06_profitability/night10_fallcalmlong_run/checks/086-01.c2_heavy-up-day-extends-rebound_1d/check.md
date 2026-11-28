---
backtest: 086-01.c2_heavy-up-day-extends-rebound_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2537 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1535 | above 0 | no |
| Mean daily return, on days in a position | 0.001467 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.054 | above 0 | yes |
| Calmar | 0.09094 | above 0.75 | no |
| Trades per day | 0.01083 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.695 % |
| Yearly return | +2.5 % (over 8.6 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-01.c2_heavy-up-day-extends-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
