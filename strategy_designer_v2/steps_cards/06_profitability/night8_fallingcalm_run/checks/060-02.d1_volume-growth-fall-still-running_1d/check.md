---
backtest: 060-02.d1_volume-growth-fall-still-running_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6004 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.04623 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007988 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4244 | above 0 | yes |
| Calmar | 0.3257 | above 0.75 | no |
| Trades per day | 0.09496 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.826 % |
| Yearly return | +8.6 % (over 7.94 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1_volume-growth-fall-still-running_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
