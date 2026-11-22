---
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8422 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.288 | above 0 | yes |
| Mean daily return | 0.0006555 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7106 | above 0 | yes |
| Calmar | 0.4746 | above 0.75 | no |
| Trades per day | 0.2446 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
