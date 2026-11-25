---
backtest: 032-02.g1.e2.e1_new-closing-high-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.535 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2161 | above 0 | no |
| Mean daily return, on days in a position | 0.005175 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.126 | above 0 | yes |
| Calmar | 13.55 | above 0.75 | yes |
| Trades per day | 0.1635 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.577 % |
| Yearly return | +404.7 % (over 1.99 years) |
| Days in a position | 92 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7c_steadydecline_run/unseen_2016_2017/backtests/032-02.g1.e2.e1_new-closing-high-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
