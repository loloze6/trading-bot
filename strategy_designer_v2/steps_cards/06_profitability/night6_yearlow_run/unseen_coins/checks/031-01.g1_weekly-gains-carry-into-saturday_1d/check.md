---
backtest: 031-01.g1_weekly-gains-carry-into-saturday_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9332 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06048 | above 0 | no |
| Mean daily return, on days in a position | 0.002509 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8197 | above 0 | yes |
| Calmar | 0.6303 | above 0.75 | no |
| Trades per day | 0.06052 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.622 % |
| Yearly return | +11.0 % (over 6.95 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_coins/backtests/031-01.g1_weekly-gains-carry-into-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
