---
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.88 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.9018 | above 0 | no |
| Mean daily return | 0.002815 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.323 | above 0 | yes |
| Calmar | 7.782 | above 0.75 | yes |
| Trades per day | 0.3377 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_range_run/unseen_2016_2017/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
