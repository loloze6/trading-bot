---
backtest: 032-01.b1.b1.e1_large-weekly-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3308 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.885 | above 0 | no |
| Mean daily return, on days in a position | -0.001286 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8178 | above 0 | no |
| Calmar | -0.1227 | above 0.75 | no |
| Trades per day | 0.01512 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.544 % |
| Yearly return | -3.9 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e1_large-weekly-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
