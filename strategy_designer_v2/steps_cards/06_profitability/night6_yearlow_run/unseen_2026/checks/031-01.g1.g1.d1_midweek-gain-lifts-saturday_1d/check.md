---
backtest: 031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4768 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3788 | above 0 | yes |
| Mean daily return, on days in a position | 0.0005728 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.06811 | above 0 | yes |
| Calmar | 0.7472 | above 0.75 | no |
| Trades per day | 0.05452 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.250 % |
| Yearly return | +2.2 % (over 0.87 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2026/backtests/031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
