---
backtest: 058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade_1d
data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.08223 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6276 | above 0 | no |
| Mean daily return, on days in a position | 0.000217 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1944 | above 0 | no |
| Calmar | 0.01636 | above 0.75 | no |
| Trades per day | 0.03325 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.357 % |
| Yearly return | +0.3 % (over 10.58 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
