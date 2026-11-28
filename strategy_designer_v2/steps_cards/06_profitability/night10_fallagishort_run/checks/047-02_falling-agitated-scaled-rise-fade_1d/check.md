---
backtest: 047-02_falling-agitated-scaled-rise-fade_1d
data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1196 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8294 | above 0 | no |
| Mean daily return, on days in a position | -0.00024 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2297 | above 0 | no |
| Calmar | -0.05596 | above 0.75 | no |
| Trades per day | 0.0673 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.568 % |
| Yearly return | -1.9 % (over 10.58 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/047-02_falling-agitated-scaled-rise-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
