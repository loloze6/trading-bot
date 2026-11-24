---
backtest: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.814 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.9375 | above 0 | no |
| Mean daily return, on days in a position | 0.004112 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.512 | above 0 | yes |
| Calmar | 7.839 | above 0.75 | yes |
| Trades per day | 0.2678 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.881 % |
| Yearly return | +158.0 % (over 1.99 years) |
| Days in a position | 67 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
