---
backtest: 074-02_calm-stretch-below-keeps-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1319 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7015 | above 0 | no |
| Mean daily return, on days in a position | -0.0002114 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.306 | above 0 | no |
| Calmar | -0.09935 | above 0.75 | no |
| Trades per day | 0.1287 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.263 % |
| Yearly return | -5.9 % (over 7.94 years) |
| Days in a position | 41 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-02_calm-stretch-below-keeps-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
