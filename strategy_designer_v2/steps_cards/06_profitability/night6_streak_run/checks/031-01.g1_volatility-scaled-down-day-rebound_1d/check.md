---
backtest: 031-01.g1_volatility-scaled-down-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6057 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.05156 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007499 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4616 | above 0 | yes |
| Calmar | 0.3635 | above 0.75 | no |
| Trades per day | 0.4813 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.112 % |
| Yearly return | +17.6 % (over 7.94 years) |
| Days in a position | 89 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.g1_volatility-scaled-down-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
