---
backtest: 048-01_scaled-up-week-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.115 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5611 | above 0 | yes |
| Mean daily return, on days in a position | 0.001224 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9305 | above 0 | yes |
| Calmar | 1.152 | above 0.75 | yes |
| Trades per day | 0.2913 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.478 % |
| Yearly return | +31.7 % (over 7.94 years) |
| Days in a position | 70 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/backtests/048-01_scaled-up-week-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
