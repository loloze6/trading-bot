---
backtest: 031-02.b1.g2.b2_unusually-large-falls-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7197 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1655 | above 0 | yes |
| Mean daily return, on days in a position | 0.000823 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5996 | above 0 | yes |
| Calmar | 0.5971 | above 0.75 | no |
| Trades per day | 0.5181 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.805 % |
| Yearly return | +20.7 % (over 7.94 years) |
| Days in a position | 83 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2.b2_unusually-large-falls-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
