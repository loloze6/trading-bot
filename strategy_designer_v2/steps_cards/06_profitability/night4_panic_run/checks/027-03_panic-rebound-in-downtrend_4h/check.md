---
backtest: 027-03_panic-rebound-in-downtrend_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1517 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.402 | above 0 | no |
| Mean daily return | 6.268e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.02834 | above 0 | yes |
| Calmar | 0.0335 | above 0.75 | no |
| Trades per day | 0.004223 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per day
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
