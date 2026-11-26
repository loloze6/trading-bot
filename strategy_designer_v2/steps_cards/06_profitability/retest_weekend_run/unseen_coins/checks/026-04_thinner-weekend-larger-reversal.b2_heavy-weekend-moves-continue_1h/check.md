---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4282 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5655 | above 0 | no |
| Mean daily return, on days in a position | 0.001608 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2625 | above 0 | yes |
| Calmar | 0.248 | above 0.75 | no |
| Trades per day | 0.04491 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.521 % |
| Yearly return | +3.8 % (over 6.95 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_coins/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
