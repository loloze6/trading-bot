---
backtest: 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.696 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.08534 | above 0 | no |
| Mean daily return, on days in a position | 0.0044 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.404 | above 0 | yes |
| Calmar | 13.41 | above 0.75 | yes |
| Trades per day | 0.02675 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.180 % |
| Yearly return | +124.3 % (over 1.99 years) |
| Days in a position | 52 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7c_rangefail_run/unseen_2016_2017/backtests/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
