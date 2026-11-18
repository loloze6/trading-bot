---
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.305 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4765 | above 0 | no |
| Mean daily return | 0.003863 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.018 | above 0 | yes |
| Calmar | 10.58 | above 0.75 | yes |
| Trades per bar | 0.1826 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
