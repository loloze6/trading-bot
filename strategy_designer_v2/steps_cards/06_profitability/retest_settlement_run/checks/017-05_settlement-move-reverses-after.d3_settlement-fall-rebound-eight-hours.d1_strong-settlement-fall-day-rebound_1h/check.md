---
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4186 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1351 | above 0 | no |
| Mean daily return, on days in a position | 0.0005131 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3086 | above 0 | yes |
| Calmar | 0.1463 | above 0.75 | no |
| Trades per day | 0.9257 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.912 % |
| Yearly return | +8.9 % (over 7.94 years) |
| Days in a position | 82 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
