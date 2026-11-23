---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.225 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.009 | above 0 | no |
| Mean daily return, on days in a position | 0.001601 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8069 | above 0 | yes |
| Calmar | 1.497 | above 0.75 | yes |
| Trades per day | 0.04053 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.421 % |
| Yearly return | +10.0 % (over 1.99 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_2016_2017/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
