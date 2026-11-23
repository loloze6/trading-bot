---
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1919 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3623 | above 0 | no |
| Mean daily return | 5.169e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.02775 | above 0 | yes |
| Calmar | 0.08529 | above 0.75 | no |
| Trades per day | 0.02186 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
