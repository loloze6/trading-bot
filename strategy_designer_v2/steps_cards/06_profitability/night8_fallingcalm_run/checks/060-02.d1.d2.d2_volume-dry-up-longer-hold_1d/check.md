---
backtest: 060-02.d1.d2.d2_volume-dry-up-longer-hold_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5659 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01171 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007443 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3438 | above 0 | yes |
| Calmar | 0.2755 | above 0.75 | no |
| Trades per day | 0.04251 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.869 % |
| Yearly return | +8.4 % (over 7.94 years) |
| Days in a position | 35 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d2.d2_volume-dry-up-longer-hold_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
