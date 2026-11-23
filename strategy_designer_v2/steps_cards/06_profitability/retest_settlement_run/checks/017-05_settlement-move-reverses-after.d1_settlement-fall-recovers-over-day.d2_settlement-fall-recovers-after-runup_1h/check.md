---
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8238 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2701 | above 0 | yes |
| Mean daily return, on days in a position | 0.001066 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7218 | above 0 | yes |
| Calmar | 0.6355 | above 0.75 | no |
| Trades per day | 0.5694 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.388 % |
| Yearly return | +20.1 % (over 7.94 years) |
| Days in a position | 56 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
