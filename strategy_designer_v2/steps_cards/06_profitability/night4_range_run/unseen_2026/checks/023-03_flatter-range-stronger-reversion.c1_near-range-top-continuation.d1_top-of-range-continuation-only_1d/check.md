---
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8282 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7302 | above 0 | yes |
| Mean daily return | 0.0007401 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.004809 | above 0 | yes |
| Calmar | 1.316 | above 0.75 | yes |
| Trades per day | 0.1443 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
