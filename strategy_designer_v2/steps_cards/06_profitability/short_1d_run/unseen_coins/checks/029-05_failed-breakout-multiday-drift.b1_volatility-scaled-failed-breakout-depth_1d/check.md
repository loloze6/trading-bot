---
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4566 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.405 | above 0 | no |
| Mean daily return, on days in a position | -0.001174 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6096 | above 0 | no |
| Calmar | -0.1404 | above 0.75 | no |
| Trades per day | 0.04981 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.945 % |
| Yearly return | -9.4 % (over 6.62 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/short_1d_run/unseen_coins/backtests/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
