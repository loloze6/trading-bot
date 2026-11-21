---
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2783 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.832 | above 0 | no |
| Mean daily return | -0.0001343 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.581 | above 0 | no |
| Calmar | -0.1393 | above 0.75 | no |
| Trades per day | 0.07001 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
