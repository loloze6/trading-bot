---
backtest: 086-01_heavy-volume-up-day-continuation_1d
data: BTC, DOT, XMR, INJ, GRT, TAO, DOGE, FIL as BTCUSD, DOTUSD, XMRUSD, INJUSD, GRTUSD, TAOUSD, DOGEUSD, FILUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6053 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1902 | above 0 | no |
| Mean daily return, on days in a position | 0.00148 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5006 | above 0 | yes |
| Calmar | 0.2468 | above 0.75 | no |
| Trades per day | 0.03885 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.583 % |
| Yearly return | +6.3 % (over 10.59 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/086-01_heavy-volume-up-day-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
