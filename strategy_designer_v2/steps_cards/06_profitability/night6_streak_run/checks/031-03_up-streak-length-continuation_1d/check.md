---
backtest: 031-03_up-streak-length-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5803 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.001406 | above 0 | no |
| Mean daily return, on days in a position | 0.000865 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4194 | above 0 | yes |
| Calmar | 0.2975 | above 0.75 | no |
| Trades per day | 0.2664 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.724 % |
| Yearly return | +18.1 % (over 7.94 years) |
| Days in a position | 96 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03_up-streak-length-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
