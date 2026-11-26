---
backtest: 033-01_range-position-drift-follows_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6484 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.09422 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006212 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5303 | above 0 | yes |
| Calmar | 0.4289 | above 0.75 | no |
| Trades per day | 0.4847 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.828 % |
| Yearly return | +18.1 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-01_range-position-drift-follows_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
