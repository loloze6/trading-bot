---
backtest: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.129 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.516 | above 0 | no |
| Mean daily return, on days in a position | 0.002648 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.941 | above 0 | yes |
| Calmar | 5.279 | above 0.75 | yes |
| Trades per day | 0.2006 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.697 % |
| Yearly return | +89.7 % (over 1.99 years) |
| Days in a position | 71 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7c_chopreversal_run/unseen_2016_2017/backtests/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
