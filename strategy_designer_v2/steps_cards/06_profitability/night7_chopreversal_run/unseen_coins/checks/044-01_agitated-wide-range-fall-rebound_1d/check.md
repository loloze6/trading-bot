---
backtest: 044-01_agitated-wide-range-fall-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.25 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2464 | above 0 | yes |
| Mean daily return, on days in a position | 0.002403 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.94 | above 0 | yes |
| Calmar | 0.7578 | above 0.75 | yes |
| Trades per day | 0.1764 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.166 % |
| Yearly return | +28.8 % (over 5.96 years) |
| Days in a position | 32 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_coins/backtests/044-01_agitated-wide-range-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
