---
backtest: 048-01_scaled-up-week-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9684 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8703 | above 0 | yes |
| Mean daily return, on days in a position | 0.001196 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.06319 | above 0 | no |
| Calmar | 1.522 | above 0.75 | yes |
| Trades per day | 0.2835 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.480 % |
| Yearly return | +26.6 % (over 0.87 years) |
| Days in a position | 63 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2026/backtests/048-01_scaled-up-week-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
