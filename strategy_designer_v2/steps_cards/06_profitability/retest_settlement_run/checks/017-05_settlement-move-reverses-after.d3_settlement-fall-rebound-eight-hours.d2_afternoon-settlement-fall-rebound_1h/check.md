---
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.02369 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5774 | above 0 | no |
| Mean daily return, on days in a position | -2.238e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1342 | above 0 | no |
| Calmar | -0.04635 | above 0.75 | no |
| Trades per day | 0.7596 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.923 % |
| Yearly return | -2.0 % (over 7.94 years) |
| Days in a position | 51 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
