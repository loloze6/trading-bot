---
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4203 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1334 | above 0 | no |
| Mean daily return, on days in a position | 0.0004578 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2983 | above 0 | yes |
| Calmar | 0.1463 | above 0.75 | no |
| Trades per day | 1.177 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.864 % |
| Yearly return | +8.9 % (over 7.94 years) |
| Days in a position | 90 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
