---
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6244 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07065 | above 0 | yes |
| Mean daily return | 6.889e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3348 | above 0 | yes |
| Calmar | 0.3376 | above 0.75 | no |
| Trades per day | 0.01215 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
