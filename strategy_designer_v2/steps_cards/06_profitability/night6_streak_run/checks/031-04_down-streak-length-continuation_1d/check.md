---
backtest: 031-04_down-streak-length-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6541 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.236 | above 0 | no |
| Mean daily return, on days in a position | -0.001029 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7957 | above 0 | no |
| Calmar | -0.398 | above 0.75 | no |
| Trades per day | 0.358 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.839 % |
| Yearly return | -39.4 % (over 7.94 years) |
| Days in a position | 94 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-04_down-streak-length-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
