---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6022 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4401 | above 0 | no |
| Mean daily return, on days in a position | 0.001194 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3863 | above 0 | yes |
| Calmar | 0.4734 | above 0.75 | no |
| Trades per day | 0.0928 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.558 % |
| Yearly return | +6.0 % (over 5.96 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_coins/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
