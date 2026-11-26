---
backtest: 047-01_falling-agitated-daily-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9283 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.261 | above 0 | no |
| Mean daily return, on days in a position | 0.001007 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4469 | above 0 | yes |
| Calmar | 1.12 | above 0.75 | yes |
| Trades per day | 0.006024 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.023 % |
| Yearly return | +0.4 % (over 1.99 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Trades per day
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/047-01_falling-agitated-daily-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
