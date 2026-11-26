---
backtest: 060-02.d1.d2.d1_volume-signal-in-deeper-falls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7165 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1623 | above 0 | yes |
| Mean daily return, on days in a position | 0.001564 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5387 | above 0 | yes |
| Calmar | 0.4126 | above 0.75 | no |
| Trades per day | 0.07521 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.965 % |
| Yearly return | +12.2 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d2.d1_volume-signal-in-deeper-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
