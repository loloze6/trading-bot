---
backtest: 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7765 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2069 | above 0 | yes |
| Mean daily return, on days in a position | 0.001416 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5732 | above 0 | yes |
| Calmar | 0.5587 | above 0.75 | no |
| Trades per day | 0.04265 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.300 % |
| Yearly return | +4.4 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
