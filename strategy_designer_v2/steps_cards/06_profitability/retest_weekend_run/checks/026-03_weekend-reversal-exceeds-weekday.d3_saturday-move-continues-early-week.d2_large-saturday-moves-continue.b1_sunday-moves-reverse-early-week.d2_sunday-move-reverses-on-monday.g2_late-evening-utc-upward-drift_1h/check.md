---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.706 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.26 | above 0 | no |
| Mean daily return, on days in a position | -0.0004631 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.831 | above 0 | no |
| Calmar | -0.2085 | above 0.75 | no |
| Trades per day | 0.9765 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.505 % |
| Yearly return | -15.6 % (over 7.94 years) |
| Days in a position | 97 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
