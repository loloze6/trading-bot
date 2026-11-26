---
backtest: 013-04_heavy-volume-below-high-breakout_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.942 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.13 | above 0 | no |
| Mean daily return, on days in a position | 0.007703 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.438 | above 0 | yes |
| Calmar | 4.988 | above 0.75 | yes |
| Trades per day | 0.03388 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.615 % |
| Yearly return | +24.8 % (over 1.99 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/volume_run/unseen_2016_2017/backtests/013-04_heavy-volume-below-high-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
