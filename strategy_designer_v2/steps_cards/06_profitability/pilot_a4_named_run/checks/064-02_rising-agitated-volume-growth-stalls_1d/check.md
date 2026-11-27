---
backtest: 064-02_rising-agitated-volume-growth-stalls_1d
data: BCH, ALGO, ZEC, INJ, FIL, TAO, PEPE, DOGE as BCHUSD, ALGOUSD, ZECUSD, INJUSD, FILUSD, TAOUSD, PEPEUSD, DOGEUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2194 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.4433 | above 0 | no |
| Mean daily return, on days in a position | -0.0005189 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3573 | above 0 | no |
| Calmar | -0.1015 | above 0.75 | no |
| Trades per day | 0.05758 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.061 % |
| Yearly return | -6.3 % (over 8.6 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/064-02_rising-agitated-volume-growth-stalls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
