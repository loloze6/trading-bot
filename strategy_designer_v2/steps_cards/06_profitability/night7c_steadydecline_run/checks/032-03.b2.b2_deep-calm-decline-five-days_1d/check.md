---
backtest: 032-03.b2.b2_deep-calm-decline-five-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.02097 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5332 | above 0 | no |
| Mean daily return, on days in a position | 2.032e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1822 | above 0 | no |
| Calmar | -0.02588 | above 0.75 | no |
| Trades per day | 0.121 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.896 % |
| Yearly return | -1.1 % (over 7.94 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b2.b2_deep-calm-decline-five-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
