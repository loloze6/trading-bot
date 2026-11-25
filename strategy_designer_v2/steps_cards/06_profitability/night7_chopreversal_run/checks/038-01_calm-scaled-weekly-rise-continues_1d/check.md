---
backtest: 038-01_calm-scaled-weekly-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8793 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3097 | above 0 | yes |
| Mean daily return, on days in a position | 0.001288 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7338 | above 0 | yes |
| Calmar | 0.6028 | above 0.75 | no |
| Trades per day | 0.1511 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.250 % |
| Yearly return | +19.9 % (over 7.94 years) |
| Days in a position | 45 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/038-01_calm-scaled-weekly-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
