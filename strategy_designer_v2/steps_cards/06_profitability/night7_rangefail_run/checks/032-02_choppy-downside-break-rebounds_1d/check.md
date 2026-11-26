---
backtest: 032-02_choppy-downside-break-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2195 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7737 | above 0 | no |
| Mean daily return, on days in a position | -0.0001604 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3676 | above 0 | no |
| Calmar | -0.05734 | above 0.75 | no |
| Trades per day | 0.004109 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.113 % |
| Yearly return | -0.5 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-02_choppy-downside-break-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
