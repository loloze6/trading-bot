---
backtest: 058-03_heavy-volume-fall-exhausts_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.08551 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4961 | above 0 | no |
| Mean daily return, on days in a position | 0.0001706 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.02907 | above 0 | no |
| Calmar | 0.009195 | above 0.75 | no |
| Trades per day | 0.03861 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.706 % |
| Yearly return | +0.3 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-03_heavy-volume-fall-exhausts_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
