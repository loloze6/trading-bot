---
plan: 002-05_short-above-long-sma-drift-up_1h
idea: 002-05_short-above-long-sma-drift-up
fit: adapted
idea verdict (branch 1): inconclusive
status: not profitable enough
---
The book: the idea traded on its own, as the backtest traded it, after the backtest's own costs.

| Bar | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6358 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4564 | above 0 | yes |
| Mean daily return | 0.0007456 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.154 | above 0 | no |
| Calmar | 0.3814 | above 0.75 | no |
| Trades per bar | 0.0355 | at least 0.01 | yes |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
- Book: BTCUSD, equal weight; 6 windows, 724 days (1.98 years); 622 trades on 17519 bars
- Holding's Sharpe: 0.1794; annualised return: 0.1987; deepest fall: 0.5209; window whose removal lowers the Sharpe most: w4
Record: `steps_cards/04_backtest/hourly_run/backtests/002-05_short-above-long-sma-drift-up_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
