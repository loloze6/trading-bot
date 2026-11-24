---
backtest: 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8554 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2995 | above 0 | yes |
| Mean daily return, on days in a position | 0.002535 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.726 | above 0 | yes |
| Calmar | 0.7695 | above 0.75 | yes |
| Trades per day | 0.04657 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.529 % |
| Yearly return | +8.5 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
