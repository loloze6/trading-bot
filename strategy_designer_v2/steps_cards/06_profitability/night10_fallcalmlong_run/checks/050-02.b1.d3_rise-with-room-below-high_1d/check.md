---
backtest: 050-02.b1.d3_rise-with-room-below-high_1d
data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1969 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2103 | above 0 | no |
| Mean daily return, on days in a position | 0.0002851 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.03007 | above 0 | no |
| Calmar | 0.04144 | above 0.75 | no |
| Trades per day | 0.0454 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.507 % |
| Yearly return | +1.4 % (over 8.6 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b1.d3_rise-with-room-below-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
