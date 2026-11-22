---
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.044 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4897 | above 0 | yes |
| Mean daily return | 0.001089 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8958 | above 0 | yes |
| Calmar | 0.9261 | above 0.75 | yes |
| Trades per day | 0.1312 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
