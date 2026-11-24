---
backtest: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7995 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2453 | above 0 | yes |
| Mean daily return, on days in a position | 0.001257 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6308 | above 0 | yes |
| Calmar | 0.7928 | above 0.75 | yes |
| Trades per day | 0.2101 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.343 % |
| Yearly return | +18.7 % (over 7.94 years) |
| Days in a position | 45 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
