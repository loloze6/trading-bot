---
backtest: 087-01_low-close-starts-unwinding_1d
data: BCH, ALGO, ZEC, INJ, FIL, TAO, PEPE, DOGE as BCHUSD, ALGOUSD, ZECUSD, INJUSD, FILUSD, TAOUSD, PEPEUSD, DOGEUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1899 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03408 | above 0 | no |
| Mean daily return, on days in a position | 0.0007364 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.03262 | above 0 | yes |
| Calmar | 0.05452 | above 0.75 | no |
| Trades per day | 0.04226 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.761 % |
| Yearly return | +1.7 % (over 8.6 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/087-01_low-close-starts-unwinding_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
