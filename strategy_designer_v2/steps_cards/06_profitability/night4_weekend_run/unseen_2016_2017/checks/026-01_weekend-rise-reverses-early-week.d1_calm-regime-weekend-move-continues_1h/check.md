---
backtest: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.004 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.331 | above 0 | no |
| Mean daily return, on days in a position | 0.00133 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3054 | above 0 | yes |
| Calmar | 1.19 | above 0.75 | yes |
| Trades per day | 0.1305 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.780 % |
| Yearly return | +14.9 % (over 1.66 years) |
| Days in a position | 31 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_2016_2017/backtests/026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
