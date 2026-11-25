---
backtest: 045-01_agitated-wide-low-close-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.165 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1616 | above 0 | yes |
| Mean daily return, on days in a position | 0.001699 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8677 | above 0 | yes |
| Calmar | 1.002 | above 0.75 | yes |
| Trades per day | 0.3342 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.311 % |
| Yearly return | +29.8 % (over 5.96 years) |
| Days in a position | 47 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_coins/backtests/045-01_agitated-wide-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
