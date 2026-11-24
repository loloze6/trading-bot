---
backtest: 031-01.g1.g1.g1_two-week-run-carries-weekend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6988 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1447 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007453 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5732 | above 0 | yes |
| Calmar | 0.454 | above 0.75 | no |
| Trades per day | 0.1852 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.859 % |
| Yearly return | +10.7 % (over 7.94 years) |
| Days in a position | 42 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1_two-week-run-carries-weekend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
