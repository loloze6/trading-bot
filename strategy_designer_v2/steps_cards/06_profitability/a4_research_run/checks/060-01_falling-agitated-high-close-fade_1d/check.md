---
backtest: 060-01_falling-agitated-high-close-fade_1d
data: BCH, AVAX, ZEC, CRV, FIL, TAO, DOGE, ONDO as BCHUSD, AVAXUSD, ZECUSD, CRVUSD, FILUSD, TAOUSD, DOGEUSD, ONDOUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.02943 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1521 | above 0 | no |
| Mean daily return, on days in a position | 5.854e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.07463 | above 0 | no |
| Calmar | -0.007102 | above 0.75 | no |
| Trades per day | 0.0745 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.494 % |
| Yearly return | -0.2 % (over 8.6 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/a4_research_run/backtests/060-01_falling-agitated-high-close-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
