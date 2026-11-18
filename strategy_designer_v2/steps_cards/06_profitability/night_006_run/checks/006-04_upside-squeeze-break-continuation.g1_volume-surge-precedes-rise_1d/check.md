---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7845 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2304 | above 0 | yes |
| Mean daily return | 0.0005775 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.649 | above 0 | yes |
| Calmar | 0.4537 | above 0.75 | no |
| Trades per bar | 0.2099 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
