---
backtest: 032-02.b1.e1.e1.e1.e3_first-break-short-follow-through_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9299 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3757 | above 0 | yes |
| Mean daily return, on days in a position | 0.003821 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7763 | above 0 | yes |
| Calmar | 1.001 | above 0.75 | yes |
| Trades per day | 0.04468 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.965 % |
| Yearly return | +16.7 % (over 7.94 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1.e3_first-break-short-follow-through_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
