---
backtest: 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d
data: XMR as XMRUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6039 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1286 | above 0 | no |
| Mean daily return, on days in a position | 0.0009398 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.3753 | above 0 | no |
| Calmar | 0.691 | above 0.75 | no |
| Trades per day | 0.3551 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.936 % |
| Yearly return | +16.8 % (over 0.87 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/unseen_2026/backtests/031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
