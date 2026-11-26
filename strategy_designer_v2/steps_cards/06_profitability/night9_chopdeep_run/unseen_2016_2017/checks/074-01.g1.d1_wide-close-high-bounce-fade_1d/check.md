---
backtest: 074-01.g1.d1_wide-close-high-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2501 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.94 | above 0 | no |
| Mean daily return, on days in a position | 0.00236 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0 | above 0 | no |
| Calmar | 0.3476 | above 0.75 | no |
| Trades per day | 0.001095 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.040 % |
| Yearly return | +0.2 % (over 1.99 years) |
| Days in a position | 0 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2016_2017/backtests/074-01.g1.d1_wide-close-high-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
