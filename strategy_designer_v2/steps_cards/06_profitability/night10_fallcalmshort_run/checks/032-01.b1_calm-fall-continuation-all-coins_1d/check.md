---
backtest: 032-01.b1_calm-fall-continuation-all-coins_1d
data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1143 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.7778 | above 0 | no |
| Mean daily return, on days in a position | 0.0003028 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1746 | above 0 | no |
| Calmar | 0.01685 | above 0.75 | no |
| Trades per day | 0.06023 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.768 % |
| Yearly return | +0.7 % (over 10.59 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/032-01.b1_calm-fall-continuation-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
