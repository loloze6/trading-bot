---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.871 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3173 | above 0 | yes |
| Mean daily return | 0.0005541 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7279 | above 0 | yes |
| Calmar | 0.7374 | above 0.75 | no |
| Trades per day | 0.9337 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
