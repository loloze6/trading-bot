---
backtest: 032-02.g1.e1.e1_raw-nearness-to-28-day-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.025 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4706 | above 0 | yes |
| Mean daily return, on days in a position | 0.001013 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8537 | above 0 | yes |
| Calmar | 1.07 | above 0.75 | yes |
| Trades per day | 0.2392 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.856 % |
| Yearly return | +35.1 % (over 7.94 years) |
| Days in a position | 98 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e1_raw-nearness-to-28-day-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
