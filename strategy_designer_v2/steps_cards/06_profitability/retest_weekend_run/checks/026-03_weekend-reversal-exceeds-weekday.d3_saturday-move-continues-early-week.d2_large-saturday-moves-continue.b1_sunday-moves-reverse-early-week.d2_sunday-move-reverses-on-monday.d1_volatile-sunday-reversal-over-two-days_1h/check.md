---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2391 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3146 | above 0 | no |
| Mean daily return, on days in a position | 0.0002126 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.08949 | above 0 | yes |
| Calmar | 0.0779 | above 0.75 | no |
| Trades per day | 0.2128 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.810 % |
| Yearly return | +2.5 % (over 7.94 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
