---
backtest: 032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5542 | above 0 | no |
| Mean daily return, on days in a position | 0 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0 | above 0 | no |
| Calmar | 0 | above 0.75 | no |
| Trades per day | 0 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.000 % |
| Yearly return | +0.0 % (over 7.94 years) |
| Days in a position | 0 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
