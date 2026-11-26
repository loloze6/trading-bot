---
backtest: 031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9543 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4002 | above 0 | yes |
| Mean daily return, on days in a position | 0.004491 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.778 | above 0 | yes |
| Calmar | 0.7602 | above 0.75 | yes |
| Trades per day | 0.03281 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.594 % |
| Yearly return | +10.7 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
