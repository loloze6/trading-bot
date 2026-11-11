---
plan: 002-02_sma-death-cross-downward-drift_1d
idea: 002-02_sma-death-cross-downward-drift
fit: adapted
verdict: inconclusive (exercise: assessed although not confirmed)
status: not worth acting on
---
Acting on it: trading the idea on its own, as the backtest traded it, after the backtest's own costs.

| Bar | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.407 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9766 | above 0 | no |
| Mean daily return | -0.000513 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5856 | above 0 | no |
| Calmar | -0.2719 | above 0.75 | no |
| Trades per bar | 0.05564 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
- Book: BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, equal weight; 24 windows, 2898 days (7.94 years); 955 trades on 17163 bars
- Holding's Sharpe: 0.5696; annualised return: -0.2551; deepest fall: 0.9383; window whose removal lowers the Sharpe most: w14
Record: `steps_cards/04_backtest/full_data_run/backtests/002-02_sma-death-cross-downward-drift_1d`
Rule: `steps_cards/06_applicability/helper/rule.yaml`
