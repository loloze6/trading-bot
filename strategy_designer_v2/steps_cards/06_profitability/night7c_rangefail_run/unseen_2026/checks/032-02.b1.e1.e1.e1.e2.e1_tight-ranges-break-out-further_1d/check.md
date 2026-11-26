---
backtest: 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.9382 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.036 | above 0 | no |
| Mean daily return, on days in a position | -0.0005968 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.246 | above 0 | no |
| Calmar | -0.7283 | above 0.75 | no |
| Trades per day | 0.009865 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.334 % |
| Yearly return | -6.0 % (over 0.87 years) |
| Days in a position | 27 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7c_rangefail_run/unseen_2026/backtests/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
