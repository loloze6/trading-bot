---
backtest: 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8761 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3219 | above 0 | yes |
| Mean daily return, on days in a position | 0.001035 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6869 | above 0 | yes |
| Calmar | 0.7752 | above 0.75 | yes |
| Trades per day | 0.01198 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.565 % |
| Yearly return | +9.3 % (over 7.94 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
