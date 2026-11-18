---
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.491 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.393 | above 0 | yes |
| Mean daily return | 0.0009514 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.559 | above 0 | yes |
| Calmar | 3.999 | above 0.75 | yes |
| Trades per bar | 0.1007 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
