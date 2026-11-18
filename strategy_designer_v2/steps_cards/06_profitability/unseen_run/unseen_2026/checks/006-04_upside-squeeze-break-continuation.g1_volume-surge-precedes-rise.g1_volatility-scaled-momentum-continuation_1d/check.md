---
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3964 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2984 | above 0 | yes |
| Mean daily return | 0.000288 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7135 | above 0 | no |
| Calmar | 0.3412 | above 0.75 | no |
| Trades per bar | 0.1854 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
