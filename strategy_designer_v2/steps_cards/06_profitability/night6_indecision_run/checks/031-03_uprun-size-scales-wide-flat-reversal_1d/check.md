---
backtest: 031-03_uprun-size-scales-wide-flat-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6472 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.201 | above 0 | no |
| Mean daily return, on days in a position | -0.001775 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8293 | above 0 | no |
| Calmar | -0.1335 | above 0.75 | no |
| Trades per day | 0.008103 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.287 % |
| Yearly return | -3.6 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-03_uprun-size-scales-wide-flat-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
