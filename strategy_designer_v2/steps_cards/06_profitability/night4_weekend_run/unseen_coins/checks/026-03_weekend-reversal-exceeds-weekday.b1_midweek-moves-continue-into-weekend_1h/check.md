---
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.287 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.7067 | above 0 | no |
| Mean daily return, on days in a position | 0.0003341 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2034 | above 0 | yes |
| Calmar | 0.105 | above 0.75 | no |
| Trades per day | 0.2346 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.842 % |
| Yearly return | +3.4 % (over 6.95 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_coins/backtests/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
