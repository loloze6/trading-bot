---
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5681 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01397 | above 0 | yes |
| Mean daily return | 0.0005684 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4579 | above 0 | yes |
| Calmar | 0.3246 | above 0.75 | no |
| Trades per bar | 0.547 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
