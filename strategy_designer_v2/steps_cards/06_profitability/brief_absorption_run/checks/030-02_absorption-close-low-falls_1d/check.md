---
backtest: 030-02_absorption-close-low-falls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6409 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.195 | above 0 | no |
| Mean daily return, on days in a position | -0.002102 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8025 | above 0 | no |
| Calmar | -0.1356 | above 0.75 | no |
| Trades per day | 0.01598 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.377 % |
| Yearly return | -4.8 % (over 7.94 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-02_absorption-close-low-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
