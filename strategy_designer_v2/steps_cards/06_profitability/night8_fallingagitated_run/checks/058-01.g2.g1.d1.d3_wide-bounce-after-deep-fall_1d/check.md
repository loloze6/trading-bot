---
backtest: 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5266 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.04304 | above 0 | no |
| Mean daily return, on days in a position | 0.001194 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4358 | above 0 | yes |
| Calmar | 0.3147 | above 0.75 | no |
| Trades per day | 0.04073 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.347 % |
| Yearly return | +3.3 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
