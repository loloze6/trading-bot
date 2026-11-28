---
backtest: 041-01.b1_rising-agitated-rise-continues_1d
data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.05243 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.8026 | above 0 | no |
| Mean daily return, on days in a position | 0.0001398 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1847 | above 0 | no |
| Calmar | -0.00457 | above 0.75 | no |
| Trades per day | 0.08346 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.747 % |
| Yearly return | -0.2 % (over 10.58 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/041-01.b1_rising-agitated-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
