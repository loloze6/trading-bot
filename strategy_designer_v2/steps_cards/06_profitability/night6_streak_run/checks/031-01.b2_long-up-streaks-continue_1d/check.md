---
backtest: 031-01.b2_long-up-streaks-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3763 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2053 | above 0 | no |
| Mean daily return, on days in a position | 0.000467 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2099 | above 0 | yes |
| Calmar | 0.1291 | above 0.75 | no |
| Trades per day | 0.3986 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.159 % |
| Yearly return | +7.3 % (over 7.94 years) |
| Days in a position | 91 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.b2_long-up-streaks-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
