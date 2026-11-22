---
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4495 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1046 | above 0 | no |
| Mean daily return | 0.001389 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.05823 | above 0 | no |
| Calmar | 0.1396 | above 0.75 | no |
| Trades per day | 0.06802 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
