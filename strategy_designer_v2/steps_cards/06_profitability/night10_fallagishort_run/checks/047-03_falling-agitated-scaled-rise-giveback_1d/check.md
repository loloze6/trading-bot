---
backtest: 047-03_falling-agitated-scaled-rise-giveback_1d
data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.04377 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.666 | above 0 | no |
| Mean daily return, on days in a position | 8.029e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.08964 | above 0 | no |
| Calmar | 0.003495 | above 0.75 | no |
| Trades per day | 0.06029 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.377 % |
| Yearly return | +0.1 % (over 10.58 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/047-03_falling-agitated-scaled-rise-giveback_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
