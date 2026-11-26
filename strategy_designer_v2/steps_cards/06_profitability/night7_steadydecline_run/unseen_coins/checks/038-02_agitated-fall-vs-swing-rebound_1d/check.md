---
backtest: 038-02_agitated-fall-vs-swing-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7995 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2043 | above 0 | no |
| Mean daily return, on days in a position | 0.001651 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5278 | above 0 | yes |
| Calmar | 0.9143 | above 0.75 | yes |
| Trades per day | 0.07553 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.530 % |
| Yearly return | +7.9 % (over 5.96 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_coins/backtests/038-02_agitated-fall-vs-swing-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
