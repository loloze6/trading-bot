---
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.435 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3157 | above 0 | no |
| Mean daily return | 0.004308 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.006 | above 0 | yes |
| Calmar | 14.88 | above 0.75 | yes |
| Trades per day | 0.1737 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
