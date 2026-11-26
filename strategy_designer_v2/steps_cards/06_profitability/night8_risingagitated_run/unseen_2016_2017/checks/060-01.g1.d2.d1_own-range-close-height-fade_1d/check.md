---
backtest: 060-01.g1.d2.d1_own-range-close-height-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2997 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.89 | above 0 | no |
| Mean daily return, on days in a position | 0.002508 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3039 | above 0 | yes |
| Calmar | 0.4318 | above 0.75 | no |
| Trades per day | 0.002191 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.070 % |
| Yearly return | +0.4 % (over 1.99 years) |
| Days in a position | 0 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_2016_2017/backtests/060-01.g1.d2.d1_own-range-close-height-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
