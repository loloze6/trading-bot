---
backtest: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.012 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.9144 | above 0 | yes |
| Mean daily return, on days in a position | 0.001214 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.582 | above 0 | yes |
| Calmar | 1.426 | above 0.75 | yes |
| Trades per day | 0.2336 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.655 % |
| Yearly return | +31.1 % (over 0.87 years) |
| Days in a position | 72 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_chopreversal_run/unseen_2026/backtests/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
