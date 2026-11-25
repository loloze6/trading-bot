---
backtest: 032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7528 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1987 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008295 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6417 | above 0 | yes |
| Calmar | 0.517 | above 0.75 | no |
| Trades per day | 0.165 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.359 % |
| Yearly return | +17.6 % (over 7.94 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
