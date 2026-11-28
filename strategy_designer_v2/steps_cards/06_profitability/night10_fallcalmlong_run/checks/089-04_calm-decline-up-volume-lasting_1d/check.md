---
backtest: 089-04_calm-decline-up-volume-lasting_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1438 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2634 | above 0 | no |
| Mean daily return, on days in a position | 0.0003037 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.01786 | above 0 | yes |
| Calmar | 0.04243 | above 0.75 | no |
| Trades per day | 0.04058 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.728 % |
| Yearly return | +1.0 % (over 8.6 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/089-04_calm-decline-up-volume-lasting_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
