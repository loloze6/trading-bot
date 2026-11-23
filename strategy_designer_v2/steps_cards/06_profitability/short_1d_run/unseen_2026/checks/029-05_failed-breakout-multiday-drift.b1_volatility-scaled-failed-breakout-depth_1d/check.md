---
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.02162 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.07642 | above 0 | no |
| Mean daily return, on days in a position | 2.24e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.137 | above 0 | no |
| Calmar | -0.03492 | above 0.75 | no |
| Trades per day | 0.05452 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.592 % |
| Yearly return | -0.4 % (over 0.87 years) |
| Days in a position | 30 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/short_1d_run/unseen_2026/backtests/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
