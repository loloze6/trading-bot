---
backtest: 031-02.b2_graded-deep-and-recent-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8431 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2889 | above 0 | yes |
| Mean daily return, on days in a position | 0.001584 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.631 | above 0 | yes |
| Calmar | 0.423 | above 0.75 | no |
| Trades per day | 0.01589 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.835 % |
| Yearly return | +13.0 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b2_graded-deep-and-recent-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
