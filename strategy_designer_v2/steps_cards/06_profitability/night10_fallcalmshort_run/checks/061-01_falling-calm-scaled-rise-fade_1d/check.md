---
backtest: 061-01_falling-calm-scaled-rise-fade_1d
data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.34 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.232 | above 0 | no |
| Mean daily return, on days in a position | -0.002868 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.402 | above 0 | no |
| Calmar | -0.09822 | above 0.75 | no |
| Trades per day | 0.00382 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.122 % |
| Yearly return | -0.8 % (over 10.59 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/061-01_falling-calm-scaled-rise-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
