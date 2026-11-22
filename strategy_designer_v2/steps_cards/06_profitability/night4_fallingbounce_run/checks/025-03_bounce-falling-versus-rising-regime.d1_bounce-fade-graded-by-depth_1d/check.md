---
backtest: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.182 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3722 | above 0 | no |
| Mean daily return | 1.985e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.05058 | above 0 | yes |
| Calmar | 0.05544 | above 0.75 | no |
| Trades per day | 0.008503 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per day
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
