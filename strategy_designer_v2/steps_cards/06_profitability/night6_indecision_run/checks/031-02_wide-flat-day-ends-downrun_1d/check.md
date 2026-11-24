---
backtest: 031-02_wide-flat-day-ends-downrun_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.04913 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.505 | above 0 | no |
| Mean daily return, on days in a position | 0.0001812 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.05986 | above 0 | no |
| Calmar | 0.001187 | above 0.75 | no |
| Trades per day | 0.01917 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.478 % |
| Yearly return | +0.0 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02_wide-flat-day-ends-downrun_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
