---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.984 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.7676 | above 0 | no |
| Mean daily return | 0.003202 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.65 | above 0 | yes |
| Calmar | 6.891 | above 0.75 | yes |
| Trades per bar | 0.2185 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
