---
backtest: 031-02.b1.b2_flat-day-after-strong-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.369 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.382 | above 0 | no |
| Mean daily return, on days in a position | 0.005934 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.088 | above 0 | yes |
| Calmar | 4.041 | above 0.75 | yes |
| Trades per day | 0.03283 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.110 % |
| Yearly return | +61.5 % (over 1.99 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-02.b1.b2_flat-day-after-strong-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
