---
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.61 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.141 | above 0 | no |
| Mean daily return | 0.004718 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.184 | above 0 | yes |
| Calmar | 18.16 | above 0.75 | yes |
| Trades per day | 0.1573 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_range_run/unseen_2016_2017/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
