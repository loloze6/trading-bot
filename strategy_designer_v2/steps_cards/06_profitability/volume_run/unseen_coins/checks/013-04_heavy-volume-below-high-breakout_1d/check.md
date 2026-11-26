---
backtest: 013-04_heavy-volume-below-high-breakout_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3891 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.757 | above 0 | no |
| Mean daily return, on days in a position | 0.003636 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.03201 | above 0 | yes |
| Calmar | 0.205 | above 0.75 | no |
| Trades per day | 0.008338 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.336 % |
| Yearly return | +2.3 % (over 5.96 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/volume_run/unseen_coins/backtests/013-04_heavy-volume-below-high-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
