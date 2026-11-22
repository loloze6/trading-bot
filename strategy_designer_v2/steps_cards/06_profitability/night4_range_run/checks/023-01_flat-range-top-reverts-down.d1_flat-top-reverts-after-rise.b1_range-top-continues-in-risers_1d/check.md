---
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9475 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3933 | above 0 | yes |
| Mean daily return | 0.0006546 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8396 | above 0 | yes |
| Calmar | 0.8792 | above 0.75 | yes |
| Trades per day | 0.2452 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
