---
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.108 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.674 | above 0 | no |
| Mean daily return, on days in a position | 0.00371 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7514 | above 0 | yes |
| Calmar | 1.225 | above 0.75 | yes |
| Trades per day | 0.06919 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.015 % |
| Yearly return | +21.6 % (over 1.99 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/volume_run/unseen_2016_2017/backtests/011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
