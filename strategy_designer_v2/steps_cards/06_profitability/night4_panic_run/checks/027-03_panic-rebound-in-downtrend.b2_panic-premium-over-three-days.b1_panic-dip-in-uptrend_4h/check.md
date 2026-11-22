---
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.091 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5375 | above 0 | yes |
| Mean daily return | 0.0002957 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.9202 | above 0 | yes |
| Calmar | 0.9264 | above 0.75 | yes |
| Trades per day | 0.02031 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
