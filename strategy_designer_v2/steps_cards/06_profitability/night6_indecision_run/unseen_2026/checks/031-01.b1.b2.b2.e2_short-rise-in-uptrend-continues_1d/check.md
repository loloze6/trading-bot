---
backtest: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9095 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8115 | above 0 | yes |
| Mean daily return, on days in a position | 0.001465 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.2875 | above 0 | no |
| Calmar | 1.888 | above 0.75 | yes |
| Trades per day | 0.1568 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.225 % |
| Yearly return | +20.6 % (over 0.87 years) |
| Days in a position | 40 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
