---
backtest: 060-02.d1.d1_volume-shrinkage-extends-running-falls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3005 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2536 | above 0 | no |
| Mean daily return, on days in a position | 0.0004928 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.06822 | above 0 | yes |
| Calmar | 0.1016 | above 0.75 | no |
| Trades per day | 0.0541 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.605 % |
| Yearly return | +2.9 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d1_volume-shrinkage-extends-running-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
