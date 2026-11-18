---
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4535 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1007 | above 0 | no |
| Mean daily return | 0.0004338 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3458 | above 0 | yes |
| Calmar | 0.1893 | above 0.75 | no |
| Trades per bar | 0.5688 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
