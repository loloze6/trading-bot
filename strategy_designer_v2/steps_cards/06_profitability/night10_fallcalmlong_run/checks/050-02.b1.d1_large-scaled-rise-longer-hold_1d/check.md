---
backtest: 050-02.b1.d1_large-scaled-rise-longer-hold_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5204 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1132 | above 0 | yes |
| Mean daily return, on days in a position | 0.001401 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3364 | above 0 | yes |
| Calmar | 0.1811 | above 0.75 | no |
| Trades per day | 0.03826 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.921 % |
| Yearly return | +7.9 % (over 8.6 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b1.d1_large-scaled-rise-longer-hold_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
