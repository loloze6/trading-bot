---
backtest: 060-01.d1_deep-dry-up-longer-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1266 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4275 | above 0 | no |
| Mean daily return, on days in a position | 0.0001898 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1108 | above 0 | no |
| Calmar | 0.01128 | above 0.75 | no |
| Trades per day | 0.04805 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.950 % |
| Yearly return | +0.7 % (over 7.94 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-01.d1_deep-dry-up-longer-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
