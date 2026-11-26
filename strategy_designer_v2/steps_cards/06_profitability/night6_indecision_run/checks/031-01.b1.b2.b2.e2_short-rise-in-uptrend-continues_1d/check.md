---
backtest: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9898 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4357 | above 0 | yes |
| Mean daily return, on days in a position | 0.001384 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7943 | above 0 | yes |
| Calmar | 0.7835 | above 0.75 | yes |
| Trades per day | 0.1849 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.283 % |
| Yearly return | +23.7 % (over 7.94 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
