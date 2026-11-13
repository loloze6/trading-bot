---
backtest: N7-01_drift-only-near-high_1d_oos3_sized
data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7206 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2728 | above 0 | yes |
| Mean daily return | 0.0004868 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.007549 | above 0 | yes |
| Calmar | 0.7646 | above 0.75 | yes |
| Trades per bar | 0.1281 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/overnight_run/backtests_sized/N7-01_drift-only-near-high_1d_oos3_sized`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
