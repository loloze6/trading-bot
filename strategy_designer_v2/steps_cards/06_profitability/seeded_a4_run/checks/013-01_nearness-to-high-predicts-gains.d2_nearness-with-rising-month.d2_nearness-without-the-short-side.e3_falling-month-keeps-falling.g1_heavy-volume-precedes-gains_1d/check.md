---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
data: XRP, TRX, ZEC, CRV, FIL, TAO, PEPE, BTC as XRPUSD, TRXUSD, ZECUSD, CRVUSD, FILUSD, TAOUSD, PEPEUSD, BTCUSD; 1d bars; windows research_2016, data use 2
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5907 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3203 | above 0 | no |
| Mean daily return, on days in a position | 0.000151 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.475 | above 0 | yes |
| Calmar | 0.2678 | above 0.75 | no |
| Trades per day | 0.398 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.484 % |
| Yearly return | +5.2 % (over 10.59 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/seeded_a4_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
