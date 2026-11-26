---
backtest: 045-01_agitated-wide-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.459 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.731 | above 0 | no |
| Mean daily return, on days in a position | 0.002152 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.031 | above 0 | yes |
| Calmar | 2.287 | above 0.75 | yes |
| Trades per day | 0.3598 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.470 % |
| Yearly return | +44.8 % (over 1.99 years) |
| Days in a position | 52 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/045-01_agitated-wide-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
