---
backtest: 032-02.g1.e2_wide-range-breakout-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.041 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.487 | above 0 | yes |
| Mean daily return, on days in a position | 0.001593 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8937 | above 0 | yes |
| Calmar | 0.8195 | above 0.75 | yes |
| Trades per day | 0.1209 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.609 % |
| Yearly return | +31.4 % (over 7.94 years) |
| Days in a position | 55 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e2_wide-range-breakout-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
