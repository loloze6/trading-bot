---
backtest: 070-01.g1_calm-decline-long-run-break_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4228 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1468 | above 0 | no |
| Mean daily return, on days in a position | 0.001707 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1303 | above 0 | yes |
| Calmar | 0.2098 | above 0.75 | no |
| Trades per day | 0.02604 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.409 % |
| Yearly return | +3.0 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1_calm-decline-long-run-break_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
