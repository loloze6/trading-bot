---
plan: 002-03_price-cross-above-sma-up_1h
idea: 002-03_price-cross-above-sma-up
fit: adapted
idea verdict (branch 1): inconclusive
status: not profitable enough
---
The book: the idea traded on its own, as the backtest traded it, after the backtest's own costs.

| Bar | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7287 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5493 | above 0 | yes |
| Mean daily return | 0.0009032 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1137 | above 0 | yes |
| Calmar | 0.6265 | above 0.75 | no |
| Trades per bar | 0.07535 | at least 0.01 | yes |

- Decided by: failed: Calmar
- Book: BTCUSD, equal weight; 6 windows, 724 days (1.98 years); 1320 trades on 17519 bars
- Holding's Sharpe: 0.1794; annualised return: 0.2602; deepest fall: 0.4153; window whose removal lowers the Sharpe most: w4
Record: `steps_cards/04_backtest/hourly_run/backtests/002-03_price-cross-above-sma-up_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
