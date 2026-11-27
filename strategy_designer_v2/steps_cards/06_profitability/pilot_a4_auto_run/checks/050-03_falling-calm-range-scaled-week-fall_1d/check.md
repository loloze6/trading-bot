---
backtest: 050-03_falling-calm-range-scaled-week-fall_1d
data: BTC, DOT, XMR, INJ, GRT, TAO, DOGE, FIL as BTCUSD, DOTUSD, XMRUSD, INJUSD, GRTUSD, TAOUSD, DOGEUSD, FILUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.04544 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.7501 | above 0 | no |
| Mean daily return, on days in a position | 0.0001129 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2552 | above 0 | no |
| Calmar | -0.013 | above 0.75 | no |
| Trades per day | 0.101 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.889 % |
| Yearly return | -0.6 % (over 10.59 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/050-03_falling-calm-range-scaled-week-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
