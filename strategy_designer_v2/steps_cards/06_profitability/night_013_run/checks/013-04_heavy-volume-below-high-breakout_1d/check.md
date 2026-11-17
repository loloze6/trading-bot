---
backtest: 013-04_heavy-volume-below-high-breakout_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5053 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.0643 | above 0 | no |
| Mean daily return | 5.91e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4019 | above 0 | yes |
| Calmar | 0.3163 | above 0.75 | no |
| Trades per bar | 0.009497 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per bar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-04_heavy-volume-below-high-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
