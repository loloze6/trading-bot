---
backtest: 031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.779 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2248 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009847 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6166 | above 0 | yes |
| Calmar | 0.506 | above 0.75 | no |
| Trades per day | 0.1619 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.816 % |
| Yearly return | +23.4 % (over 7.94 years) |
| Days in a position | 75 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
