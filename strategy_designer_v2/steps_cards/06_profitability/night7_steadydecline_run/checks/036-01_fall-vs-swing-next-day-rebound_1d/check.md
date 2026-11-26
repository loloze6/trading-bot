---
backtest: 036-01_fall-vs-swing-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6934 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1393 | above 0 | yes |
| Mean daily return, on days in a position | 0.00199 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5426 | above 0 | yes |
| Calmar | 0.5561 | above 0.75 | no |
| Trades per day | 0.1094 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.217 % |
| Yearly return | +14.3 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/036-01_fall-vs-swing-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
