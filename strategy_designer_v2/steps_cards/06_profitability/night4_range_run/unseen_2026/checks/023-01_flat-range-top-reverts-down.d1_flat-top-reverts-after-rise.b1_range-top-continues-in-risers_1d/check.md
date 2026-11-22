---
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.367 | above 0 | yes |
| Sharpe minus holding's Sharpe | 2.269 | above 0 | yes |
| Mean daily return | 0.001408 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.261 | above 0 | yes |
| Calmar | 8.773 | above 0.75 | yes |
| Trades per day | 0.188 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
