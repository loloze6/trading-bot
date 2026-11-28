---
backtest: 086-02.c1_forceful-break-day-continues_1d
data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4325 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4225 | above 0 | no |
| Mean daily return, on days in a position | 0.001712 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.07413 | above 0 | yes |
| Calmar | 0.234 | above 0.75 | no |
| Trades per day | 0.03084 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.859 % |
| Yearly return | +6.1 % (over 10.58 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/086-02.c1_forceful-break-day-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
