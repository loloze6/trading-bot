---
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.69 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.061 | above 0 | no |
| Mean daily return, on days in a position | 0.002375 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.461 | above 0 | yes |
| Calmar | 3.604 | above 0.75 | yes |
| Trades per day | 0.1724 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.349 % |
| Yearly return | +49.7 % (over 1.99 years) |
| Days in a position | 50 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/volume_run/unseen_2016_2017/backtests/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
