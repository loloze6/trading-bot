---
backtest: 031-01.g1.g1_midweek-run-carries-into-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5747 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.02058 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006992 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3797 | above 0 | yes |
| Calmar | 0.2472 | above 0.75 | no |
| Trades per day | 0.1205 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.566 % |
| Yearly return | +5.8 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1_midweek-run-carries-into-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
