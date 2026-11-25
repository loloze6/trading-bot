---
backtest: 052-01_down-day-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6427 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.08856 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008076 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4891 | above 0 | yes |
| Calmar | 0.4934 | above 0.75 | no |
| Trades per day | 0.4226 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.803 % |
| Yearly return | +17.5 % (over 7.94 years) |
| Days in a position | 75 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/052-01_down-day-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
