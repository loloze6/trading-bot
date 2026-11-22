---
backtest: 027-01_panic-range-multiple-rebound_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6966 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1428 | above 0 | yes |
| Mean daily return | 0.001463 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5496 | above 0 | yes |
| Calmar | 0.3301 | above 0.75 | no |
| Trades per day | 0.02185 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-01_panic-range-multiple-rebound_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
