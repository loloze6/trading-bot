---
backtest: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d
data: NEAR, ONDO, SUI, TAO as NEARUSD, ONDOUSD, SUIUSD, TAOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9511 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1861 | above 0 | yes |
| Mean daily return, on days in a position | 0.00283 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5149 | above 0 | yes |
| Calmar | 1.099 | above 0.75 | yes |
| Trades per day | 0.09836 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.144 % |
| Yearly return | +36.3 % (over 2.65 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/validation_run/unseen_coins/backtests/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
