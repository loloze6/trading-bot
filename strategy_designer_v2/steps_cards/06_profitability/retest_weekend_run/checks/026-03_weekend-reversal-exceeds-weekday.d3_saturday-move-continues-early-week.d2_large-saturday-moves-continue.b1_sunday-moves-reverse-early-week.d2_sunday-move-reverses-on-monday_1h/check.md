---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.118 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4358 | above 0 | no |
| Mean daily return, on days in a position | 9.917e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.01694 | above 0 | yes |
| Calmar | 0.0416 | above 0.75 | no |
| Trades per day | 0.2096 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.608 % |
| Yearly return | +0.7 % (over 7.94 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
