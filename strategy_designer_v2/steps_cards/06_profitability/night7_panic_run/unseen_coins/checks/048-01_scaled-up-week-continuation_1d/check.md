---
backtest: 048-01_scaled-up-week-continuation_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.32 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3267 | above 0 | yes |
| Mean daily return, on days in a position | 0.002015 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.109 | above 0 | yes |
| Calmar | 1.49 | above 0.75 | yes |
| Trades per day | 0.2938 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.667 % |
| Yearly return | +45.0 % (over 6.95 years) |
| Days in a position | 57 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/unseen_coins/backtests/048-01_scaled-up-week-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
