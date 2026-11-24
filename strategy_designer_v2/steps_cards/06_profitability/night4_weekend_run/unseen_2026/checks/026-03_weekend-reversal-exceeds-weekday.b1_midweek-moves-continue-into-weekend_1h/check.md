---
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3216 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2235 | above 0 | yes |
| Mean daily return, on days in a position | 0.0005405 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1856 | above 0 | no |
| Calmar | 0.2032 | above 0.75 | no |
| Trades per day | 0.2409 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.374 % |
| Yearly return | +5.2 % (over 0.87 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_2026/backtests/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
