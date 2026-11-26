---
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5198 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4545 | above 0 | no |
| Mean daily return, on days in a position | 0.0008297 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3399 | above 0 | yes |
| Calmar | 0.2978 | above 0.75 | no |
| Trades per day | 0.2281 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.232 % |
| Yearly return | +9.9 % (over 6.95 years) |
| Days in a position | 40 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night_run/unseen_coins/backtests/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
