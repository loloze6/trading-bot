---
backtest: 031-01.b1.b2_wide-day-extends-strong-run_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9132 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.359 | above 0 | yes |
| Mean daily return, on days in a position | 0.001188 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.755 | above 0 | yes |
| Calmar | 0.673 | above 0.75 | no |
| Trades per day | 0.2915 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.745 % |
| Yearly return | +28.3 % (over 7.94 years) |
| Days in a position | 70 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2_wide-day-extends-strong-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
