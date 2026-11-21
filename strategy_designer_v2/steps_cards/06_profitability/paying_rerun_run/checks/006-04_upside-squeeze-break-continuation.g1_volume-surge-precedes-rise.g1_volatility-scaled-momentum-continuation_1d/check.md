---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.022 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4676 | above 0 | yes |
| Mean daily return | 0.0008663 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8536 | above 0 | yes |
| Calmar | 0.9434 | above 0.75 | yes |
| Trades per day | 0.1912 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
