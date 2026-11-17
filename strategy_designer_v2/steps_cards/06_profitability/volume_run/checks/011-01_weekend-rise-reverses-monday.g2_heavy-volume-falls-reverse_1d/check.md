---
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9228 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3687 | above 0 | yes |
| Mean daily return | 0.0004207 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.8362 | above 0 | yes |
| Calmar | 0.8146 | above 0.75 | yes |
| Trades per bar | 0.06454 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/volume_run/backtests/011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
