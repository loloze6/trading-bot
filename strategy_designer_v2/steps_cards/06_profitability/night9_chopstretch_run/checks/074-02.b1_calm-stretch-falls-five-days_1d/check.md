---
backtest: 074-02.b1_calm-stretch-falls-five-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.05912 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5105 | above 0 | no |
| Mean daily return, on days in a position | 9.863e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.114 | above 0 | no |
| Calmar | -0.02168 | above 0.75 | no |
| Trades per day | 0.1575 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.060 % |
| Yearly return | -0.8 % (over 7.94 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-02.b1_calm-stretch-falls-five-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
