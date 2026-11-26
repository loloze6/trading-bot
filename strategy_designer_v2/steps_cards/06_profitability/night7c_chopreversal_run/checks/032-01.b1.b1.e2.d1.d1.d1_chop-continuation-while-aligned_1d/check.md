---
backtest: 032-01.b1.b1.e2.d1.d1.d1_chop-continuation-while-aligned_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4659 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.08829 | above 0 | no |
| Mean daily return, on days in a position | 0.0004864 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2994 | above 0 | yes |
| Calmar | 0.2687 | above 0.75 | no |
| Trades per day | 0.301 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.153 % |
| Yearly return | +8.2 % (over 7.94 years) |
| Days in a position | 58 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d1.d1_chop-continuation-while-aligned_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
