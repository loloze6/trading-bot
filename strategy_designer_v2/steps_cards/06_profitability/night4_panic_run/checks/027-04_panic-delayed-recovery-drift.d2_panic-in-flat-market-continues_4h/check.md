---
backtest: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4307 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9845 | above 0 | no |
| Mean daily return | -0.0006983 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5731 | above 0 | no |
| Calmar | -0.3646 | above 0.75 | no |
| Trades per day | 0.07378 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
