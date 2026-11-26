---
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.149 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.9 | above 0 | no |
| Mean daily return, on days in a position | -0.003493 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.966 | above 0 | no |
| Calmar | -0.3867 | above 0.75 | no |
| Trades per day | 0.0106 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.328 % |
| Yearly return | -7.1 % (over 1.99 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/short_1d_run/unseen_2016_2017/backtests/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
