---
backtest: 039-02_agitated-range-fall-low-close-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.115 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1108 | above 0 | yes |
| Mean daily return, on days in a position | 0.002109 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7753 | above 0 | yes |
| Calmar | 0.6845 | above 0.75 | no |
| Trades per day | 0.1885 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.210 % |
| Yearly return | +26.0 % (over 5.96 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_coins/backtests/039-02_agitated-range-fall-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
