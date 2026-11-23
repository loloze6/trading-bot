---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.393 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.024 | above 0 | no |
| Mean daily return, on days in a position | 0.003741 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.363 | above 0 | yes |
| Calmar | 6.71 | above 0.75 | yes |
| Trades per day | 0.05464 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.505 % |
| Yearly return | +13.9 % (over 1.32 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_2016_2017/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
