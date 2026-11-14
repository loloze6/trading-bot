---
backtest: N7-01_drift-only-near-high_1d_sized
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.052 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4979 | above 0 | yes |
| Mean daily return | 0.0007928 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.918 | above 0 | yes |
| Calmar | 0.8876 | above 0.75 | yes |
| Trades per bar | 0.1507 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests_sized/N7-01_drift-only-near-high_1d_sized`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
