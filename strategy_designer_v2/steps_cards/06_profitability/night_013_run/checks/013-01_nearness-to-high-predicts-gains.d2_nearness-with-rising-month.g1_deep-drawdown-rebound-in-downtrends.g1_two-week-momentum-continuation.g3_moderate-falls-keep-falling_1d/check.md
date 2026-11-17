---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2201 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.334 | above 0 | no |
| Mean daily return | 4.21e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.02273 | above 0 | yes |
| Calmar | 0.06966 | above 0.75 | no |
| Trades per bar | 0.1319 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
