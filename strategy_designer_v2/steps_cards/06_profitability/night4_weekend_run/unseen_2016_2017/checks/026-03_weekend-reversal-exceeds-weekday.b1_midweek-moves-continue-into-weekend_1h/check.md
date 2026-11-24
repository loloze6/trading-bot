---
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4088 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.643 | above 0 | no |
| Mean daily return, on days in a position | -0.0003848 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7202 | above 0 | no |
| Calmar | -0.3071 | above 0.75 | no |
| Trades per day | 0.216 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.899 % |
| Yearly return | -8.1 % (over 1.99 years) |
| Days in a position | 50 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_2016_2017/backtests/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
