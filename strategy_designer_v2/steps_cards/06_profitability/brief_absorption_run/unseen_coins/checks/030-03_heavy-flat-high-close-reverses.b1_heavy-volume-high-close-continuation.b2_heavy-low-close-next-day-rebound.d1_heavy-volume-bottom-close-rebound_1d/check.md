---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9822 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.0115 | above 0 | no |
| Mean daily return, on days in a position | 0.002013 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8421 | above 0 | yes |
| Calmar | 0.9049 | above 0.75 | yes |
| Trades per day | 0.05408 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.383 % |
| Yearly return | +7.2 % (over 6.95 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/brief_absorption_run/unseen_coins/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
