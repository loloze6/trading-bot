---
backtest: 054-01_deep-reclaimed-low-pierce-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2574 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3122 | above 0 | no |
| Mean daily return, on days in a position | 0.002583 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.09146 | above 0 | yes |
| Calmar | 0.2023 | above 0.75 | no |
| Trades per day | 0.007167 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.472 % |
| Yearly return | +1.9 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-01_deep-reclaimed-low-pierce-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
