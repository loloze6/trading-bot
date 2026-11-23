---
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.736 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.834 | above 0 | no |
| Mean daily return, on days in a position | -0.01031 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.995 | above 0 | no |
| Calmar | -1.082 | above 0.75 | no |
| Trades per day | 0.005711 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.177 % |
| Yearly return | -5.7 % (over 0.87 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/short_1d_run/unseen_2026/backtests/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
