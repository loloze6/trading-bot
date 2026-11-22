---
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9937 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4395 | above 0 | yes |
| Mean daily return | 0.0008772 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8414 | above 0 | yes |
| Calmar | 0.863 | above 0.75 | yes |
| Trades per day | 0.1509 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
