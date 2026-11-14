---
plan: 002-01_sma-golden-cross-upward-drift_1d
idea: 002-01_sma-golden-cross-upward-drift
fit: adapted
verdict: inconclusive (exercise: assessed although not confirmed)
status: not worth acting on
---
Acting on it: trading the idea on its own, as the backtest traded it, after the backtest's own costs.

| Bar | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3762 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1934 | above 0 | no |
| Mean daily return | 0.0007398 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.03304 | above 0 | yes |
| Calmar | 0.0009771 | above 0.75 | no |
| Trades per bar | 0.04207 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
- Book: BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, equal weight; 24 windows, 2898 days (7.94 years); 722 trades on 17163 bars
- Holding's Sharpe: 0.5696; annualised return: 0.0009097; deepest fall: 0.931; window whose removal lowers the Sharpe most: w11
Record: `steps_cards/04_backtest/full_data_run/backtests/002-01_sma-golden-cross-upward-drift_1d`
Rule: `steps_cards/06_applicability/helper/rule.yaml`
