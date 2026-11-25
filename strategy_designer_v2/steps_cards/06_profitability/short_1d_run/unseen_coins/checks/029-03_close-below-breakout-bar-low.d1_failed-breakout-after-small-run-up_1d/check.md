---
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1256 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.119 | above 0 | no |
| Mean daily return, on days in a position | -0.0007909 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2861 | above 0 | no |
| Calmar | -0.03933 | above 0.75 | no |
| Trades per day | 0.005474 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.227 % |
| Yearly return | -0.6 % (over 6.95 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/short_1d_run/unseen_coins/backtests/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
