---
plan: 001-01_rsi-high-extreme-reversal-down_1h
idea: 001-01_rsi-high-extreme-reversal-down
fit: adapted
verdict: inconclusive (exercise: assessed although not confirmed)
status: not worth acting on
---
Acting on it: trading the idea on its own, as the backtest traded it, after the backtest's own costs.

| Bar | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.936 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.002 | above 0 | no |
| Mean daily return | -0.00408 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -3.35 | above 0 | no |
| Calmar | -0.8336 | above 0.75 | no |
| Trades per bar | 0.2196 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
- Book: BTCUSD, ETHUSD, equal weight; 6 windows, 724 days (1.98 years); 7693 trades on 35038 bars
- Holding's Sharpe: 0.06572; annualised return: -0.8038; deepest fall: 0.9643; window whose removal lowers the Sharpe most: w2
Record: `steps_cards/04_backtest/hourly_run/backtests/001-01_rsi-high-extreme-reversal-down_1h`
Rule: `steps_cards/06_applicability/helper/rule.yaml`
