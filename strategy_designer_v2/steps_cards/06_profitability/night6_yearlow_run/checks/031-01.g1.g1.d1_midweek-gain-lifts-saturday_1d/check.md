---
backtest: 031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.11 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5554 | above 0 | yes |
| Mean daily return, on days in a position | 0.002384 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9246 | above 0 | yes |
| Calmar | 0.8801 | above 0.75 | yes |
| Trades per day | 0.063 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.517 % |
| Yearly return | +11.1 % (over 7.94 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
