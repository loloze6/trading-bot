---
backtest: N4-01_breakout-drift-lasts_1d
data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6995 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.202 | above 0 | yes |
| Mean daily return | 0.0003983 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.02078 | above 0 | yes |
| Calmar | 0.6221 | above 0.75 | no |
| Trades per bar | 0.1482 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/backtests/N4-01_breakout-drift-lasts_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
