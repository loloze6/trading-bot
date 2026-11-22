---
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5045 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.04924 | above 0 | no |
| Mean daily return | 0.0007888 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3369 | above 0 | yes |
| Calmar | 0.1823 | above 0.75 | no |
| Trades per day | 0.948 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
