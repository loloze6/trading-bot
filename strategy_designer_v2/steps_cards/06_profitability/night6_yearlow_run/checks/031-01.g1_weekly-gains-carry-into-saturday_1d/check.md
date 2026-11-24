---
backtest: 031-01.g1_weekly-gains-carry-into-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.007 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4529 | above 0 | yes |
| Mean daily return, on days in a position | 0.002281 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8759 | above 0 | yes |
| Calmar | 1.008 | above 0.75 | yes |
| Trades per day | 0.06146 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.532 % |
| Yearly return | +10.2 % (over 7.94 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1_weekly-gains-carry-into-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
