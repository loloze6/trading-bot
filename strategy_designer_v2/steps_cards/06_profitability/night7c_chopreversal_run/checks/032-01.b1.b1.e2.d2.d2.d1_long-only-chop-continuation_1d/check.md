---
backtest: 032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.035 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4808 | above 0 | yes |
| Mean daily return, on days in a position | 0.001558 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8391 | above 0 | yes |
| Calmar | 1.066 | above 0.75 | yes |
| Trades per day | 0.09809 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.369 % |
| Yearly return | +26.7 % (over 7.94 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
