---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.034 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03833 | above 0 | no |
| Mean daily return | 0.003358 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.623 | above 0 | yes |
| Calmar | 11.31 | above 0.75 | yes |
| Trades per bar | 0.2361 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
