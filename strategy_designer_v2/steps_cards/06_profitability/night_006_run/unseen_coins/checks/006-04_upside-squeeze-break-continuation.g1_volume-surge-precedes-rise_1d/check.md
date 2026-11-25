---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9086 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.0851 | above 0 | no |
| Mean daily return, on days in a position | 0.001564 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6897 | above 0 | yes |
| Calmar | 0.7442 | above 0.75 | no |
| Trades per day | 0.2196 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.449 % |
| Yearly return | +23.8 % (over 6.95 years) |
| Days in a position | 44 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night_006_run/unseen_coins/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
