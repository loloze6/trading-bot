---
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9246 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3704 | above 0 | yes |
| Mean daily return | 0.0007638 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7972 | above 0 | yes |
| Calmar | 0.5097 | above 0.75 | no |
| Trades per day | 0.2192 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
