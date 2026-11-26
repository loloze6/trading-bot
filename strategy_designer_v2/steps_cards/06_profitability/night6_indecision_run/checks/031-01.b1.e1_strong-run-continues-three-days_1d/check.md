---
backtest: 031-01.b1.e1_strong-run-continues-three-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.019 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4651 | above 0 | yes |
| Mean daily return, on days in a position | 0.001118 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.837 | above 0 | yes |
| Calmar | 0.9466 | above 0.75 | yes |
| Trades per day | 0.3236 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.509 % |
| Yearly return | +28.7 % (over 7.94 years) |
| Days in a position | 72 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.e1_strong-run-continues-three-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
