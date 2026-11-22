---
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1445 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6987 | above 0 | no |
| Mean daily return | -9.125e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2594 | above 0 | no |
| Calmar | -0.1028 | above 0.75 | no |
| Trades per day | 0.0545 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
