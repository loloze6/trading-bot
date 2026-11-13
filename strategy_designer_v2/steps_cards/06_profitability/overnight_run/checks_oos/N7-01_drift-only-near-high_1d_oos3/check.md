---
backtest: N7-01_drift-only-near-high_1d_oos3
data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7893 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3415 | above 0 | yes |
| Mean daily return | 0.00145 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.07623 | above 0 | yes |
| Calmar | 0.6959 | above 0.75 | no |
| Trades per bar | 0.1363 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N7-01_drift-only-near-high_1d_oos3`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
