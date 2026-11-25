---
backtest: 032-04_calm-decline-rally-sold_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.06252 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4916 | above 0 | no |
| Mean daily return, on days in a position | 7.792e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.0862 | above 0 | no |
| Calmar | -0.007041 | above 0.75 | no |
| Trades per day | 0.06072 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.781 % |
| Yearly return | -0.2 % (over 7.94 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-04_calm-decline-rally-sold_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
