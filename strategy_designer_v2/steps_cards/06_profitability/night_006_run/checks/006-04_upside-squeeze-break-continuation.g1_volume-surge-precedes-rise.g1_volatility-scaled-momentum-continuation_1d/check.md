---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9692 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.415 | above 0 | yes |
| Mean daily return | 0.0007647 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.821 | above 0 | yes |
| Calmar | 0.8235 | above 0.75 | yes |
| Trades per bar | 0.1955 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
