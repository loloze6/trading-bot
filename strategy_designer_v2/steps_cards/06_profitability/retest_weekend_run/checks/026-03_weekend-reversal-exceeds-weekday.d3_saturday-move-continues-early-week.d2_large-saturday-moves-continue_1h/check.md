---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3684 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1853 | above 0 | no |
| Mean daily return, on days in a position | 0.0003872 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2338 | above 0 | yes |
| Calmar | 0.1459 | above 0.75 | no |
| Trades per day | 0.1431 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.775 % |
| Yearly return | +4.5 % (over 7.94 years) |
| Days in a position | 39 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
