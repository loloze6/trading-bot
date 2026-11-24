---
backtest: 031-01.g1.d1_rebound-grows-with-volatility_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.261 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.52 | above 0 | no |
| Mean daily return, on days in a position | 0.005752 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9342 | above 0 | yes |
| Calmar | 2.325 | above 0.75 | yes |
| Trades per day | 0.0271 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.497 % |
| Yearly return | +12.2 % (over 1.99 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.g1.d1_rebound-grows-with-volatility_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
