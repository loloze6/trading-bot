---
backtest: 041-01.b1_rising-agitated-rise-continues_1d
data: BCH, ALGO, ZEC, INJ, FIL, TAO, PEPE, DOGE as BCHUSD, ALGOUSD, ZECUSD, INJUSD, FILUSD, TAOUSD, PEPEUSD, DOGEUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.05712 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1668 | above 0 | no |
| Mean daily return, on days in a position | 0.0001379 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2196 | above 0 | no |
| Calmar | -0.002486 | above 0.75 | no |
| Trades per day | 0.08262 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.672 % |
| Yearly return | -0.1 % (over 8.6 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/041-01.b1_rising-agitated-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
