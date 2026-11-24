---
backtest: 031-04_yearly-low-break-reverses_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6565 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07485 | above 0 | yes |
| Mean daily return, on days in a position | 0.001 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4966 | above 0 | yes |
| Calmar | 0.7495 | above 0.75 | no |
| Trades per day | 0.001232 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.056 % |
| Yearly return | +0.7 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-04_yearly-low-break-reverses_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
