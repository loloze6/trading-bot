---
backtest: 047-03.c1_rally-near-30-day-high-fades_1d
data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.0795 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6303 | above 0 | no |
| Mean daily return, on days in a position | 0.000127 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.05229 | above 0 | no |
| Calmar | 0.01281 | above 0.75 | no |
| Trades per day | 0.04346 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.413 % |
| Yearly return | +0.3 % (over 10.58 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/047-03.c1_rally-near-30-day-high-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
