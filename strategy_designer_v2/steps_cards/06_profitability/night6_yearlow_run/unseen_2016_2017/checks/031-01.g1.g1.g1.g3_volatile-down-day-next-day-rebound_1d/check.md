---
backtest: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6974 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.374 | above 0 | no |
| Mean daily return, on days in a position | 0.001297 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3742 | above 0 | yes |
| Calmar | 0.6524 | above 0.75 | no |
| Trades per day | 0.09035 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.744 % |
| Yearly return | +9.3 % (over 1.99 years) |
| Days in a position | 21 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
