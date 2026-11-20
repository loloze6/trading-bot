---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.421 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3305 | above 0 | no |
| Mean daily return | 0.003681 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.036 | above 0 | yes |
| Calmar | 9.899 | above 0.75 | yes |
| Trades per day | 0.1874 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/hold_paying_run/unseen_2016_2017/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
