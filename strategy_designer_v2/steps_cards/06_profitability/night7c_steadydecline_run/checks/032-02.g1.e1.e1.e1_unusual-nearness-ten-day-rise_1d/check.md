---
backtest: 032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.839 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2848 | above 0 | yes |
| Mean daily return, on days in a position | 0.0002434 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6152 | above 0 | yes |
| Calmar | 0.5963 | above 0.75 | no |
| Trades per day | 0.1207 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.547 % |
| Yearly return | +8.6 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
