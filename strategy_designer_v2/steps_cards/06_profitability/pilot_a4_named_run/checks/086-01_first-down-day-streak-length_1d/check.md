---
backtest: 086-01_first-down-day-streak-length_1d
data: BCH, ALGO, ZEC, INJ, FIL, TAO, PEPE, DOGE as BCHUSD, ALGOUSD, ZECUSD, INJUSD, FILUSD, TAOUSD, PEPEUSD, DOGEUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.817 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.041 | above 0 | no |
| Mean daily return, on days in a position | -0.002045 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9634 | above 0 | no |
| Calmar | -0.1377 | above 0.75 | no |
| Trades per day | 0.04171 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.472 % |
| Yearly return | -7.5 % (over 8.6 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/086-01_first-down-day-streak-length_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
