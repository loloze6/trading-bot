---
backtest: 031-04_downrun-size-scales-wide-flat-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1774 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7316 | above 0 | no |
| Mean daily return, on days in a position | -0.0007799 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3508 | above 0 | no |
| Calmar | -0.05175 | above 0.75 | no |
| Trades per day | 0.00388 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.282 % |
| Yearly return | -1.1 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-04_downrun-size-scales-wide-flat-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
