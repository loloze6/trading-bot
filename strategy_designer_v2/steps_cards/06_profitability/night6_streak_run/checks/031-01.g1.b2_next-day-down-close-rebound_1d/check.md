---
backtest: 031-01.g1.b2_next-day-down-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7936 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2394 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008696 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6388 | above 0 | yes |
| Calmar | 0.7305 | above 0.75 | no |
| Trades per day | 0.3896 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.475 % |
| Yearly return | +20.1 % (over 7.94 years) |
| Days in a position | 70 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.g1.b2_next-day-down-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
