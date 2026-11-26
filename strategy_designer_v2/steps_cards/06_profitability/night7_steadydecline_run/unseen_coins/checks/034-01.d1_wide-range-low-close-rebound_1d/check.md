---
backtest: 034-01.d1_wide-range-low-close-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.139 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1352 | above 0 | yes |
| Mean daily return, on days in a position | 0.001742 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8365 | above 0 | yes |
| Calmar | 0.9795 | above 0.75 | yes |
| Trades per day | 0.3262 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.372 % |
| Yearly return | +30.3 % (over 5.96 years) |
| Days in a position | 47 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_coins/backtests/034-01.d1_wide-range-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
