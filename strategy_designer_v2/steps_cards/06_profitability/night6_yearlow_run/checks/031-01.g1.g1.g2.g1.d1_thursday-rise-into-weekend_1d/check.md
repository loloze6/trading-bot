---
backtest: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.31 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7554 | above 0 | yes |
| Mean daily return, on days in a position | 0.002048 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.137 | above 0 | yes |
| Calmar | 1.712 | above 0.75 | yes |
| Trades per day | 0.08953 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.788 % |
| Yearly return | +20.4 % (over 7.94 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
