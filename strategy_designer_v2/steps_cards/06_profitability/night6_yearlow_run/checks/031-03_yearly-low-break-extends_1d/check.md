---
backtest: 031-03_yearly-low-break-extends_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5393 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.121 | above 0 | no |
| Mean daily return, on days in a position | -0.0003503 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.602 | above 0 | no |
| Calmar | -0.1111 | above 0.75 | no |
| Trades per day | 0.004048 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.059 % |
| Yearly return | -0.6 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-03_yearly-low-break-extends_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
