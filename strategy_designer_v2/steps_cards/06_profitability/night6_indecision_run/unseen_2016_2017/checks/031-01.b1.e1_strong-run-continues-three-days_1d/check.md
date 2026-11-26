---
backtest: 031-01.b1.e1_strong-run-continues-three-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.942 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.809 | above 0 | no |
| Mean daily return, on days in a position | 0.003663 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.548 | above 0 | yes |
| Calmar | 8.203 | above 0.75 | yes |
| Trades per day | 0.3536 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.877 % |
| Yearly return | +169.4 % (over 1.99 years) |
| Days in a position | 79 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.b1.e1_strong-run-continues-three-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
