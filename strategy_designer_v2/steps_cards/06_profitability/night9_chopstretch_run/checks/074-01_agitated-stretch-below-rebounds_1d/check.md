---
backtest: 074-01_agitated-stretch-below-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6037 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03407 | above 0 | yes |
| Mean daily return, on days in a position | 0.001034 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.458 | above 0 | yes |
| Calmar | 0.3841 | above 0.75 | no |
| Trades per day | 0.09788 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.161 % |
| Yearly return | +11.5 % (over 7.94 years) |
| Days in a position | 35 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-01_agitated-stretch-below-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
