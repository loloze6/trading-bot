---
backtest: N4-01_breakout-drift-lasts_1d_oos3
data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7139 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2164 | above 0 | yes |
| Mean daily return | 0.0003912 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.05665 | above 0 | yes |
| Calmar | 0.5948 | above 0.75 | no |
| Trades per bar | 0.1612 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-01_breakout-drift-lasts_1d_oos3`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
