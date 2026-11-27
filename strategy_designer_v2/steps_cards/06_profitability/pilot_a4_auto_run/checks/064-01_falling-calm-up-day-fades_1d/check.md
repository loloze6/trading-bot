---
backtest: 064-01_falling-calm-up-day-fades_1d
data: BTC, DOT, XMR, INJ, GRT, TAO, DOGE, FIL as BTCUSD, DOTUSD, XMRUSD, INJUSD, GRTUSD, TAOUSD, DOGEUSD, FILUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6103 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.406 | above 0 | no |
| Mean daily return, on days in a position | -0.001133 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8124 | above 0 | no |
| Calmar | -0.1293 | above 0.75 | no |
| Trades per day | 0.09565 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.726 % |
| Yearly return | -9.0 % (over 10.59 years) |
| Days in a position | 20 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/064-01_falling-calm-up-day-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
