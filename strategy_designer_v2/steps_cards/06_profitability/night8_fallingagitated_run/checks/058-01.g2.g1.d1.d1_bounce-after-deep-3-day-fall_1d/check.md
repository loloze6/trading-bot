---
backtest: 058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5683 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.00135 | above 0 | no |
| Mean daily return, on days in a position | 0.001536 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4741 | above 0 | yes |
| Calmar | 0.4062 | above 0.75 | no |
| Trades per day | 0.03869 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.379 % |
| Yearly return | +3.9 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
