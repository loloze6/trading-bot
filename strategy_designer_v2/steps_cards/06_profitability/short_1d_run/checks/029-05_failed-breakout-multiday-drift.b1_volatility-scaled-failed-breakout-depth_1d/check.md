---
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3871 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.167 | above 0 | no |
| Mean daily return | 0.000164 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2477 | above 0 | yes |
| Calmar | 0.1903 | above 0.75 | no |
| Trades per day | 0.04656 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
