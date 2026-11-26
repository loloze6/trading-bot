---
backtest: 031-01.b1_wide-day-extends-up-run_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9011 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.347 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009337 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7355 | above 0 | yes |
| Calmar | 0.7564 | above 0.75 | yes |
| Trades per day | 0.3747 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.496 % |
| Yearly return | +24.2 % (over 7.94 years) |
| Days in a position | 76 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1_wide-day-extends-up-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
