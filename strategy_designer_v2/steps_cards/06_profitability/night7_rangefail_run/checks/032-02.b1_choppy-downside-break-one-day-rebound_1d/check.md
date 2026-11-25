---
backtest: 032-02.b1_choppy-downside-break-one-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3197 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2345 | above 0 | no |
| Mean daily return, on days in a position | 0.0003721 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1595 | above 0 | yes |
| Calmar | 0.22 | above 0.75 | no |
| Trades per day | 0.002967 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.034 % |
| Yearly return | +0.2 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-02.b1_choppy-downside-break-one-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
