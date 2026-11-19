---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5453 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.008421 | above 0 | no |
| Mean daily return | 0.0004299 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3814 | above 0 | yes |
| Calmar | 0.2304 | above 0.75 | no |
| Trades per day | 1.826 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
