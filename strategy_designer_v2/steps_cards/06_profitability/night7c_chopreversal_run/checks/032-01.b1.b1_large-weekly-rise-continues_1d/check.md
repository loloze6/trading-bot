---
backtest: 032-01.b1.b1_large-weekly-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9857 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4315 | above 0 | yes |
| Mean daily return, on days in a position | 0.002287 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8589 | above 0 | yes |
| Calmar | 0.776 | above 0.75 | yes |
| Trades per day | 0.02659 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.781 % |
| Yearly return | +14.6 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1_large-weekly-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
