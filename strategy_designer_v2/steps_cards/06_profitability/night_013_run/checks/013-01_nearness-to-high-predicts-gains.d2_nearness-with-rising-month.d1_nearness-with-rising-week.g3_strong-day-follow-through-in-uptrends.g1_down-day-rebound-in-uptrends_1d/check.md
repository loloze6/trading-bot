---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5652 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01105 | above 0 | yes |
| Mean daily return | 0.000219 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3788 | above 0 | yes |
| Calmar | 0.3017 | above 0.75 | no |
| Trades per bar | 0.176 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
