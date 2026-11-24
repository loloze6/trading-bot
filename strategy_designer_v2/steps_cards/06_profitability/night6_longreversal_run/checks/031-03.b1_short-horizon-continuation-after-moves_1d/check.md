---
backtest: 031-03.b1_short-horizon-continuation-after-moves_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4435 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1107 | above 0 | no |
| Mean daily return, on days in a position | 0.0004542 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3081 | above 0 | yes |
| Calmar | 0.1548 | above 0.75 | no |
| Trades per day | 0.3112 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.954 % |
| Yearly return | +10.1 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.b1_short-horizon-continuation-after-moves_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
