---
backtest: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5413 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.01246 | above 0 | no |
| Mean daily return | 0.0005458 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3989 | above 0 | yes |
| Calmar | 0.2781 | above 0.75 | no |
| Trades per day | 0.8289 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
