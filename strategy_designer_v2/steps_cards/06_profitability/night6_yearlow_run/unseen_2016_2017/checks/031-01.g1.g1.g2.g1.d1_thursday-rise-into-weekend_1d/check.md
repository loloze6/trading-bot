---
backtest: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.264 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.487 | above 0 | no |
| Mean daily return, on days in a position | 0.001788 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.036 | above 0 | yes |
| Calmar | 1.719 | above 0.75 | yes |
| Trades per day | 0.1159 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.844 % |
| Yearly return | +21.0 % (over 1.99 years) |
| Days in a position | 31 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
