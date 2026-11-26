---
backtest: 041-02_wide-down-day-next-day-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8574 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1363 | above 0 | no |
| Mean daily return, on days in a position | 0.0009212 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6666 | above 0 | yes |
| Calmar | 0.7906 | above 0.75 | yes |
| Trades per day | 0.4056 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.547 % |
| Yearly return | +23.2 % (over 6.95 years) |
| Days in a position | 75 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_panic_run/unseen_coins/backtests/041-02_wide-down-day-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
