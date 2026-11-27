---
backtest: 086-02_first-down-day-run-size_1d
data: BCH, ALGO, ZEC, INJ, FIL, TAO, PEPE, DOGE as BCHUSD, ALGOUSD, ZECUSD, INJUSD, FILUSD, TAOUSD, PEPEUSD, DOGEUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6754 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8993 | above 0 | no |
| Mean daily return, on days in a position | -0.001521 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8483 | above 0 | no |
| Calmar | -0.1335 | above 0.75 | no |
| Trades per day | 0.06108 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.624 % |
| Yearly return | -8.4 % (over 8.6 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/086-02_first-down-day-run-size_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
