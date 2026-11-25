---
backtest: 041-03_agitated-fall-drop-vs-range-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.098 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.092 | above 0 | no |
| Mean daily return, on days in a position | 0.001925 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4127 | above 0 | yes |
| Calmar | 1.44 | above 0.75 | yes |
| Trades per day | 0.008762 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.055 % |
| Yearly return | +1.2 % (over 1.99 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Trades per day
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2016_2017/backtests/041-03_agitated-fall-drop-vs-range-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
