---
backtest: 045-01_rising-market-late-week-gain_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.503 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5287 | above 0 | yes |
| Mean daily return, on days in a position | 0.004031 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.214 | above 0 | yes |
| Calmar | 1.569 | above 0.75 | yes |
| Trades per day | 0.07197 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.832 % |
| Yearly return | +25.4 % (over 6.95 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/unseen_coins/backtests/045-01_rising-market-late-week-gain_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
