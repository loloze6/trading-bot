---
backtest: 031-02.b1_wide-flat-day-continues-uprun_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5585 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.004367 | above 0 | yes |
| Mean daily return, on days in a position | 0.001734 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4379 | above 0 | yes |
| Calmar | 0.4632 | above 0.75 | no |
| Trades per day | 0.007704 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.424 % |
| Yearly return | +4.3 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1_wide-flat-day-continues-uprun_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
