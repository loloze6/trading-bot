---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.081 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5002 | above 0 | yes |
| Mean daily return, on days in a position | 0.001211 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.912 | above 0 | yes |
| Calmar | 0.6089 | above 0.75 | no |
| Trades per day | 0.1138 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.543 % |
| Yearly return | +11.3 % (over 7.94 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
