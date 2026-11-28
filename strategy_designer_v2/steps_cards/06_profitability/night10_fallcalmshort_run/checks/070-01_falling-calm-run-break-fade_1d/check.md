---
backtest: 070-01_falling-calm-run-break-fade_1d
data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1521 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.74 | above 0 | no |
| Mean daily return, on days in a position | 0.0007988 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1985 | above 0 | no |
| Calmar | 0.06211 | above 0.75 | no |
| Trades per day | 0.02553 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.519 % |
| Yearly return | +1.1 % (over 10.59 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/070-01_falling-calm-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
