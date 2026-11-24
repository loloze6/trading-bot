---
backtest: 031-02_down-streak-length-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5688 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.0146 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009264 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4093 | above 0 | yes |
| Calmar | 0.2754 | above 0.75 | no |
| Trades per day | 0.3017 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.979 % |
| Yearly return | +17.2 % (over 7.94 years) |
| Days in a position | 96 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02_down-streak-length-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
