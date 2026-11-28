---
backtest: 090-01_calm-decline-scaled-push-continues_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4247 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01746 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008766 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2633 | above 0 | yes |
| Calmar | 0.1371 | above 0.75 | no |
| Trades per day | 0.06099 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.628 % |
| Yearly return | +4.5 % (over 8.6 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/090-01_calm-decline-scaled-push-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
