---
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8042 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7062 | above 0 | yes |
| Mean daily return | 0.0006301 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.103 | above 0 | no |
| Calmar | 1.174 | above 0.75 | yes |
| Trades per day | 0.1542 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
