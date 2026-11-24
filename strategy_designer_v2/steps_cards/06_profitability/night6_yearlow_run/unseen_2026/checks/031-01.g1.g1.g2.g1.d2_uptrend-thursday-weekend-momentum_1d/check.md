---
backtest: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7698 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6718 | above 0 | yes |
| Mean daily return, on days in a position | 0.002884 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.443 | above 0 | yes |
| Calmar | 1.439 | above 0.75 | yes |
| Trades per day | 0.05556 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.832 % |
| Yearly return | +11.7 % (over 0.87 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2026/backtests/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
