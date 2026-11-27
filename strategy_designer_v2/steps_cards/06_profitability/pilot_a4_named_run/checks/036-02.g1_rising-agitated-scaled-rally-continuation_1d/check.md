---
backtest: 036-02.g1_rising-agitated-scaled-rally-continuation_1d
data: BCH, ALGO, ZEC, INJ, FIL, TAO, PEPE, DOGE as BCHUSD, ALGOUSD, ZECUSD, INJUSD, FILUSD, TAOUSD, PEPEUSD, DOGEUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5998 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3758 | above 0 | yes |
| Mean daily return, on days in a position | 0.003316 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3169 | above 0 | yes |
| Calmar | 0.3095 | above 0.75 | no |
| Trades per day | 0.0315 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.820 % |
| Yearly return | +8.5 % (over 8.6 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/036-02.g1_rising-agitated-scaled-rally-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
