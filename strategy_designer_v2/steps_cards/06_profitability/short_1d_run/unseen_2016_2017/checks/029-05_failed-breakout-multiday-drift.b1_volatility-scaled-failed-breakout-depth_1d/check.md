---
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.834 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.916 | above 0 | no |
| Mean daily return, on days in a position | -0.003408 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.239 | above 0 | no |
| Calmar | -0.5582 | above 0.75 | no |
| Trades per day | 0.05578 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.015 % |
| Yearly return | -31.3 % (over 1.99 years) |
| Days in a position | 29 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/short_1d_run/unseen_2016_2017/backtests/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
