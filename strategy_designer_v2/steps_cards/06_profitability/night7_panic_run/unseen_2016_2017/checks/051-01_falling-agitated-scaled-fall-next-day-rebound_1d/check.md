---
backtest: 051-01_falling-agitated-scaled-fall-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.869 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.321 | above 0 | no |
| Mean daily return, on days in a position | 0.0009631 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4942 | above 0 | yes |
| Calmar | 0.9045 | above 0.75 | yes |
| Trades per day | 0.007119 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.028 % |
| Yearly return | +0.5 % (over 1.99 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Trades per day
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2016_2017/backtests/051-01_falling-agitated-scaled-fall-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
