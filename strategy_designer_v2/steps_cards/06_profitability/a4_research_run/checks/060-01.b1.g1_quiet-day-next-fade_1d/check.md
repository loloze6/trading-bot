---
backtest: 060-01.b1.g1_quiet-day-next-fade_1d
data: BCH, AVAX, ZEC, CRV, FIL, TAO, DOGE, ONDO as BCHUSD, AVAXUSD, ZECUSD, CRVUSD, FILUSD, TAOUSD, DOGEUSD, ONDOUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.818 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.426 | above 0 | no |
| Mean daily return, on days in a position | -0.000995 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.142 | above 0 | no |
| Calmar | -0.1894 | above 0.75 | no |
| Trades per day | 0.1785 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.947 % |
| Yearly return | -15.2 % (over 9.27 years) |
| Days in a position | 41 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/a4_research_run/backtests/060-01.b1.g1_quiet-day-next-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
