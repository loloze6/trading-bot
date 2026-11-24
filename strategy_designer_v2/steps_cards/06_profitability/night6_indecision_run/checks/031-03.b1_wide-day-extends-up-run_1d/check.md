---
backtest: 031-03.b1_wide-day-extends-up-run_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.03 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4758 | above 0 | yes |
| Mean daily return, on days in a position | 0.002068 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8339 | above 0 | yes |
| Calmar | 1.099 | above 0.75 | yes |
| Trades per day | 0.08468 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.967 % |
| Yearly return | +18.9 % (over 7.94 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-03.b1_wide-day-extends-up-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
