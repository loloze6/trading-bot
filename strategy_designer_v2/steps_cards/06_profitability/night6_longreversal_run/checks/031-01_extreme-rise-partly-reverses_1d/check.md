---
backtest: 031-01_extreme-rise-partly-reverses_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.826 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.408 | above 0 | no |
| Mean daily return, on days in a position | -0.002041 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9663 | above 0 | no |
| Calmar | -0.2948 | above 0.75 | no |
| Trades per day | 0.02805 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.702 % |
| Yearly return | -27.5 % (over 7.94 years) |
| Days in a position | 36 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-01_extreme-rise-partly-reverses_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
