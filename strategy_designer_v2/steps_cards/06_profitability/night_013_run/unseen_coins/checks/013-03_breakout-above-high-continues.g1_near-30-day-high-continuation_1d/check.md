---
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9872 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.006461 | above 0 | no |
| Mean daily return, on days in a position | 0.000341 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7979 | above 0 | yes |
| Calmar | 1.252 | above 0.75 | yes |
| Trades per day | 0.1563 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.642 % |
| Yearly return | +12.0 % (over 6.95 years) |
| Days in a position | 97 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position
Record: `steps_cards/04_backtest/night_013_run/unseen_coins/backtests/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
