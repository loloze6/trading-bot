---
backtest: 086-01_down-day-volume-share-drift_1d
data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2211 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.113 | above 0 | no |
| Mean daily return, on days in a position | -0.0005649 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5433 | above 0 | no |
| Calmar | -0.1026 | above 0.75 | no |
| Trades per day | 0.08016 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.874 % |
| Yearly return | -4.9 % (over 10.59 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/086-01_down-day-volume-share-drift_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
