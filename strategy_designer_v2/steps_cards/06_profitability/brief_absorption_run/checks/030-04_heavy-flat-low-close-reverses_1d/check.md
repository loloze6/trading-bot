---
backtest: 030-04_heavy-flat-low-close-reverses_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.08811 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6423 | above 0 | no |
| Mean daily return, on days in a position | -0.0002436 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4045 | above 0 | no |
| Calmar | -0.06341 | above 0.75 | no |
| Trades per day | 0.04074 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.805 % |
| Yearly return | -2.5 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-04_heavy-flat-low-close-reverses_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
