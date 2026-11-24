---
backtest: 036-01_scaled-rally-week-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7159 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1617 | above 0 | yes |
| Mean daily return, on days in a position | 0.001037 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5428 | above 0 | yes |
| Calmar | 0.3833 | above 0.75 | no |
| Trades per day | 0.2017 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.317 % |
| Yearly return | +24.4 % (over 7.94 years) |
| Days in a position | 84 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/036-01_scaled-rally-week-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
