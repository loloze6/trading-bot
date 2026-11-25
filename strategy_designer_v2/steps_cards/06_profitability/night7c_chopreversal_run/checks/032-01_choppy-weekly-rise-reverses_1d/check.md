---
backtest: 032-01_choppy-weekly-rise-reverses_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7249 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.295 | above 0 | no |
| Mean daily return, on days in a position | -0.0007299 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8345 | above 0 | no |
| Calmar | -0.1678 | above 0.75 | no |
| Trades per day | 0.08099 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.755 % |
| Yearly return | -10.9 % (over 7.94 years) |
| Days in a position | 39 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01_choppy-weekly-rise-reverses_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
