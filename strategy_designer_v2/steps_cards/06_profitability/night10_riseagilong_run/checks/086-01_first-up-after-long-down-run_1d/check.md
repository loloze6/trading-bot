---
backtest: 086-01_first-up-after-long-down-run_1d
data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2803 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5747 | above 0 | no |
| Mean daily return, on days in a position | 0.001162 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.06661 | above 0 | yes |
| Calmar | 0.1053 | above 0.75 | no |
| Trades per day | 0.03515 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.020 % |
| Yearly return | +3.7 % (over 10.58 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/086-01_first-up-after-long-down-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
