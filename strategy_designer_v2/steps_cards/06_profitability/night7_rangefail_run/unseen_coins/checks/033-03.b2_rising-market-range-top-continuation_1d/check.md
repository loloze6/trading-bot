---
backtest: 033-03.b2_rising-market-range-top-continuation_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.975 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.01872 | above 0 | no |
| Mean daily return, on days in a position | 0.001667 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8041 | above 0 | yes |
| Calmar | 0.9088 | above 0.75 | yes |
| Trades per day | 0.1996 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.484 % |
| Yearly return | +26.7 % (over 6.95 years) |
| Days in a position | 45 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_coins/backtests/033-03.b2_rising-market-range-top-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
