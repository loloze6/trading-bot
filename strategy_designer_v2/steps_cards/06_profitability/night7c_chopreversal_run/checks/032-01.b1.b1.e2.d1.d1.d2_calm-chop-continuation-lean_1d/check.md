---
backtest: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8687 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3145 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008577 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7629 | above 0 | yes |
| Calmar | 0.7518 | above 0.75 | yes |
| Trades per day | 0.2393 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.477 % |
| Yearly return | +22.8 % (over 7.94 years) |
| Days in a position | 78 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
