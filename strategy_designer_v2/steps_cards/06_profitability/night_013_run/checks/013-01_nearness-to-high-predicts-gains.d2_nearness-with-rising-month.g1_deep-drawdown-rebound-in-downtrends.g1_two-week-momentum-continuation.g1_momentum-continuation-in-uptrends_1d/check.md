---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.146 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5914 | above 0 | yes |
| Mean daily return | 0.0007619 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9856 | above 0 | yes |
| Calmar | 1.535 | above 0.75 | yes |
| Trades per bar | 0.1522 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
