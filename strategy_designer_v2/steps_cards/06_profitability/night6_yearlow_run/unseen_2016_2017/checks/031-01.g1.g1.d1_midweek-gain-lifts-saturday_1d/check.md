---
backtest: 031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.433 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.318 | above 0 | no |
| Mean daily return, on days in a position | 0.0008825 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.07251 | above 0 | yes |
| Calmar | 0.3054 | above 0.75 | no |
| Trades per day | 0.07558 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.597 % |
| Yearly return | +4.4 % (over 1.99 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
