---
backtest: 032-01.b1_calm-fall-continuation-all-coins_1d
data: BTC, DOT, XMR, INJ, GRT, TAO, DOGE, FIL as BTCUSD, DOTUSD, XMRUSD, INJUSD, GRTUSD, TAOUSD, DOGEUSD, FILUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1091 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9046 | above 0 | no |
| Mean daily return, on days in a position | -0.0002317 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4067 | above 0 | no |
| Calmar | -0.05144 | above 0.75 | no |
| Trades per day | 0.07336 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.756 % |
| Yearly return | -2.6 % (over 10.59 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/032-01.b1_calm-fall-continuation-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
