---
backtest: 033-03.b2_rising-market-range-top-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.427 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.324 | above 0 | no |
| Mean daily return, on days in a position | 0.003754 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.111 | above 0 | yes |
| Calmar | 10.84 | above 0.75 | yes |
| Trades per day | 0.2801 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.588 % |
| Yearly return | +169.9 % (over 1.99 years) |
| Days in a position | 76 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2016_2017/backtests/033-03.b2_rising-market-range-top-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
