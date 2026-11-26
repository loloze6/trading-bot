---
backtest: 031-01.b2.b1_long-up-streaks-ten-day-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7444 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1627 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007951 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5938 | above 0 | yes |
| Calmar | 0.5436 | above 0.75 | no |
| Trades per day | 0.1001 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.993 % |
| Yearly return | +23.5 % (over 7.94 years) |
| Days in a position | 98 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.b2.b1_long-up-streaks-ten-day-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
