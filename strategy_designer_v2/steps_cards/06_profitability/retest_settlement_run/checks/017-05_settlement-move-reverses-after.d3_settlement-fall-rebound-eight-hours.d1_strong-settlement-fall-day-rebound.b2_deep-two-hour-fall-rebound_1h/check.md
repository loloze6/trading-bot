---
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.677 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1232 | above 0 | yes |
| Mean daily return, on days in a position | 0.0012 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5309 | above 0 | yes |
| Calmar | 0.3766 | above 0.75 | no |
| Trades per day | 0.3169 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 3.385 % |
| Yearly return | +25.3 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
