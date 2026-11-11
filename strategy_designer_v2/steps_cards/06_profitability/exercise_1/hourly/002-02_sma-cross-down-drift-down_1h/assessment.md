---
plan: 002-02_sma-cross-down-drift-down_1h
idea: 002-02_sma-cross-down-drift-down
fit: adapted
verdict: inconclusive (exercise: assessed although not confirmed)
status: not worth acting on
---
Acting on it: trading the idea on its own, as the backtest traded it, after the backtest's own costs.

| Bar | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4611 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2817 | above 0 | yes |
| Mean daily return | 0.0007919 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1328 | above 0 | no |
| Calmar | 0.2142 | above 0.75 | no |
| Trades per bar | 0.04127 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
- Book: BTCUSD, equal weight; 6 windows, 724 days (1.98 years); 723 trades on 17519 bars
- Holding's Sharpe: 0.1794; annualised return: 0.1138; deepest fall: 0.5312; window whose removal lowers the Sharpe most: w2
Record: `steps_cards/04_backtest/hourly_run/backtests/002-02_sma-cross-down-drift-down_1h`
Rule: `steps_cards/06_applicability/helper/rule.yaml`
