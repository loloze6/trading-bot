---
backtest: 032-01_choppy-agitated-weekly-rise-reverts_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6712 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.241 | above 0 | no |
| Mean daily return, on days in a position | -0.0008396 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7623 | above 0 | no |
| Calmar | -0.1231 | above 0.75 | no |
| Trades per day | 0.02249 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.352 % |
| Yearly return | -4.6 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/032-01_choppy-agitated-weekly-rise-reverts_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
