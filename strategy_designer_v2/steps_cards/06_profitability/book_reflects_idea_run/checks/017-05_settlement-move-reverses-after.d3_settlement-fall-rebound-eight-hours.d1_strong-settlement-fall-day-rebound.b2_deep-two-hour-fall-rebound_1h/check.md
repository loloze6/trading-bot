---
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3869 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1668 | above 0 | no |
| Mean daily return, on days in a position | 0.0007104 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2376 | above 0 | yes |
| Calmar | 0.09732 | above 0.75 | no |
| Trades per day | 0.7632 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.650 % |
| Yearly return | +6.6 % (over 7.94 years) |
| Days in a position | 76 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/book_reflects_idea_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
