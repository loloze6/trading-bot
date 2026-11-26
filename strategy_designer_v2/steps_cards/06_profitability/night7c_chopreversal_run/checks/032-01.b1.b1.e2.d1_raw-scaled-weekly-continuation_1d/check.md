---
backtest: 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5217 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03248 | above 0 | no |
| Mean daily return, on days in a position | 0.0004765 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4237 | above 0 | yes |
| Calmar | 0.3003 | above 0.75 | no |
| Trades per day | 0.3456 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.561 % |
| Yearly return | +11.8 % (over 7.94 years) |
| Days in a position | 89 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
