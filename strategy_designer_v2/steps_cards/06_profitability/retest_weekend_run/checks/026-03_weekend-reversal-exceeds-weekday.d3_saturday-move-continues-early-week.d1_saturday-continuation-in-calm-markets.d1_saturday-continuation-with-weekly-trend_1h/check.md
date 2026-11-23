---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.029 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4477 | above 0 | yes |
| Mean daily return, on days in a position | 0.001784 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9212 | above 0 | yes |
| Calmar | 0.8457 | above 0.75 | yes |
| Trades per day | 0.07287 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.519 % |
| Yearly return | +10.2 % (over 7.94 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
