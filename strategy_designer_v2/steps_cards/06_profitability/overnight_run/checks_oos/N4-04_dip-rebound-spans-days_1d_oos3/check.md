---
backtest: N4-04_dip-rebound-spans-days_1d_oos3
data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6189 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1711 | above 0 | yes |
| Mean daily return | 0.0005839 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.5133 | above 0 | no |
| Calmar | 0.6185 | above 0.75 | no |
| Trades per bar | 0.07841 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-04_dip-rebound-spans-days_1d_oos3`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
