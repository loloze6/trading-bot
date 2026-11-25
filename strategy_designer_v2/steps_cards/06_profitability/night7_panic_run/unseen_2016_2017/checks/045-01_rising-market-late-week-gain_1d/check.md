---
backtest: 045-01_rising-market-late-week-gain_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.107 | above 0 | yes |
| Sharpe minus holding's Sharpe | -2.675 | above 0 | no |
| Mean daily return, on days in a position | 0.002169 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7746 | above 0 | yes |
| Calmar | 1.614 | above 0.75 | yes |
| Trades per day | 0.1095 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.045 % |
| Yearly return | +22.2 % (over 1.99 years) |
| Days in a position | 28 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2016_2017/backtests/045-01_rising-market-late-week-gain_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
