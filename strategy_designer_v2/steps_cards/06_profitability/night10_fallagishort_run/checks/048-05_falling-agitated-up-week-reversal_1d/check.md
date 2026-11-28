---
backtest: 048-05_falling-agitated-up-week-reversal_1d
data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.08523 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.795 | above 0 | no |
| Mean daily return, on days in a position | -0.0001884 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.166 | above 0 | no |
| Calmar | -0.03959 | above 0.75 | no |
| Trades per day | 0.03926 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.343 % |
| Yearly return | -0.8 % (over 10.58 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/048-05_falling-agitated-up-week-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
