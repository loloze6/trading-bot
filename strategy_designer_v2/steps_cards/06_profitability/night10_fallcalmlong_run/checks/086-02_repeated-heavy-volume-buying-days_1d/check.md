---
backtest: 086-02_repeated-heavy-volume-buying-days_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.03408 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.4413 | above 0 | no |
| Mean daily return, on days in a position | -0.0001013 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1518 | above 0 | no |
| Calmar | -0.038 | above 0.75 | no |
| Trades per day | 0.03309 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.554 % |
| Yearly return | -0.9 % (over 8.6 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-02_repeated-heavy-volume-buying-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
