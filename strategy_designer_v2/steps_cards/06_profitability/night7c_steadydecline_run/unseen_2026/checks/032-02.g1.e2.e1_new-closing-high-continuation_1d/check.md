---
backtest: 032-02.g1.e2.e1_new-closing-high-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7981 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009285 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.09924 | above 0 | no |
| Calmar | 1.071 | above 0.75 | yes |
| Trades per day | 0.1449 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.712 % |
| Yearly return | +23.2 % (over 0.87 years) |
| Days in a position | 77 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night7c_steadydecline_run/unseen_2026/backtests/032-02.g1.e2.e1_new-closing-high-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
