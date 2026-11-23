---
backtest: 030-03_heavy-flat-high-close-reverses_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4986 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.053 | above 0 | no |
| Mean daily return, on days in a position | -0.001574 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8205 | above 0 | no |
| Calmar | -0.1303 | above 0.75 | no |
| Trades per day | 0.01586 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.380 % |
| Yearly return | -3.8 % (over 7.94 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
