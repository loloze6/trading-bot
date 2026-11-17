---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4886 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06558 | above 0 | no |
| Mean daily return | 0.0004982 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.391 | above 0 | yes |
| Calmar | 0.2277 | above 0.75 | no |
| Trades per bar | 0.528 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
