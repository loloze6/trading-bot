---
backtest: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4436 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1102 | above 0 | no |
| Mean daily return | 0.0005937 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.275 | above 0 | yes |
| Calmar | 0.1331 | above 0.75 | no |
| Trades per day | 0.03555 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
