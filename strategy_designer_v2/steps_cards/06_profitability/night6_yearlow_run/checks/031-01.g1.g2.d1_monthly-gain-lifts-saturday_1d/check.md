---
backtest: 031-01.g1.g2.d1_monthly-gain-lifts-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8621 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.308 | above 0 | yes |
| Mean daily return, on days in a position | 0.002132 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7034 | above 0 | yes |
| Calmar | 0.715 | above 0.75 | no |
| Trades per day | 0.05838 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.553 % |
| Yearly return | +8.9 % (over 7.94 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g2.d1_monthly-gain-lifts-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
