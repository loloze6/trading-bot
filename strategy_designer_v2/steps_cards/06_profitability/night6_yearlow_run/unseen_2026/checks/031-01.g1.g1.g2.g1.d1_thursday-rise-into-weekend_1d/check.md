---
backtest: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8026 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7045 | above 0 | yes |
| Mean daily return, on days in a position | 0.001759 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2543 | above 0 | yes |
| Calmar | 1.265 | above 0.75 | yes |
| Trades per day | 0.0919 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.848 % |
| Yearly return | +12.5 % (over 0.87 years) |
| Days in a position | 20 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2026/backtests/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
