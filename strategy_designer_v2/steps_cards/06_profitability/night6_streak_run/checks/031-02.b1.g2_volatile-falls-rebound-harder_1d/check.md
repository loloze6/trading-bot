---
backtest: 031-02.b1.g2_volatile-falls-rebound-harder_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7096 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1555 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009997 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5965 | above 0 | yes |
| Calmar | 0.5902 | above 0.75 | no |
| Trades per day | 0.5154 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.242 % |
| Yearly return | +23.5 % (over 7.94 years) |
| Days in a position | 83 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2_volatile-falls-rebound-harder_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
