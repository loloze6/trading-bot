---
backtest: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.242 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6875 | above 0 | yes |
| Mean daily return | 0.0005232 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.033 | above 0 | yes |
| Calmar | 1.127 | above 0.75 | yes |
| Trades per day | 0.04508 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
