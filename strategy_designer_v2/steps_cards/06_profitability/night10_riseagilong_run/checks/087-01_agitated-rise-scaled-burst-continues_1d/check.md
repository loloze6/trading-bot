---
backtest: 087-01_agitated-rise-scaled-burst-continues_1d
data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2209 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6341 | above 0 | no |
| Mean daily return, on days in a position | 0.001825 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.0004128 | above 0 | no |
| Calmar | 0.04751 | above 0.75 | no |
| Trades per day | 0.0216 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.907 % |
| Yearly return | +2.4 % (over 10.58 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/087-01_agitated-rise-scaled-burst-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
