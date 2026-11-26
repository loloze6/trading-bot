---
backtest: 013-04_heavy-volume-below-high-breakout_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8696 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7716 | above 0 | yes |
| Mean daily return, on days in a position | 0.006332 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3115 | above 0 | yes |
| Calmar | 1.564 | above 0.75 | yes |
| Trades per day | 0.004673 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.130 % |
| Yearly return | +2.2 % (over 0.87 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Trades per day
Record: `steps_cards/04_backtest/volume_run/unseen_2026/backtests/013-04_heavy-volume-below-high-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
