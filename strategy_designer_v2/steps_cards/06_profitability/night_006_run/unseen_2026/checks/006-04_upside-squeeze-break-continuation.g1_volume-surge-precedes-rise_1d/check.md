---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.9247 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.023 | above 0 | no |
| Mean daily return, on days in a position | -0.001323 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.983 | above 0 | no |
| Calmar | -0.721 | above 0.75 | no |
| Trades per day | 0.1921 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.602 % |
| Yearly return | -28.1 % (over 0.87 years) |
| Days in a position | 59 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_006_run/unseen_2026/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
