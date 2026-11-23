---
backtest: 030-01_absorption-close-high-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.009056 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5632 | above 0 | no |
| Mean daily return, on days in a position | -2.702e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1357 | above 0 | no |
| Calmar | -0.02447 | above 0.75 | no |
| Trades per day | 0.03641 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.802 % |
| Yearly return | -1.3 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-01_absorption-close-high-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
