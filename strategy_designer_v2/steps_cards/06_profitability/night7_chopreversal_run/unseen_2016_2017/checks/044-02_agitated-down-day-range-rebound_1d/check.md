---
backtest: 044-02_agitated-down-day-range-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7715 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.418 | above 0 | no |
| Mean daily return, on days in a position | 0.001214 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4176 | above 0 | yes |
| Calmar | 0.8145 | above 0.75 | yes |
| Trades per day | 0.1796 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.092 % |
| Yearly return | +14.9 % (over 1.99 years) |
| Days in a position | 36 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/044-02_agitated-down-day-range-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
