---
backtest: 064-01_falling-calm-up-day-fades_1d
data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6883 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.58 | above 0 | no |
| Mean daily return, on days in a position | -0.001414 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9349 | above 0 | no |
| Calmar | -0.1404 | above 0.75 | no |
| Trades per day | 0.08092 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.668 % |
| Yearly return | -9.2 % (over 10.59 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/064-01_falling-calm-up-day-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
