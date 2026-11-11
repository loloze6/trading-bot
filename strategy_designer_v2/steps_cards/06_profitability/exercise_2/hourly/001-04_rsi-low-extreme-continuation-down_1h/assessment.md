---
plan: 001-04_rsi-low-extreme-continuation-down_1h
idea: 001-04_rsi-low-extreme-continuation-down
fit: adapted
idea verdict (branch 1): inconclusive
status: not profitable enough
---
The book: the idea traded on its own, as the backtest traded it, after the backtest's own costs.

| Bar | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.6 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.665 | above 0 | no |
| Mean daily return | -0.003086 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.348 | above 0 | no |
| Calmar | -0.7844 | above 0.75 | no |
| Trades per bar | 0.1895 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
- Book: BTCUSD, ETHUSD, equal weight; 6 windows, 724 days (1.98 years); 6640 trades on 35038 bars
- Holding's Sharpe: 0.06572; annualised return: -0.744; deepest fall: 0.9485; window whose removal lowers the Sharpe most: w2
Record: `steps_cards/04_backtest/hourly_run/backtests/001-04_rsi-low-extreme-continuation-down_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
