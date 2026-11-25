---
backtest: 033-03.b2_rising-market-range-top-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.919 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3648 | above 0 | yes |
| Mean daily return, on days in a position | 0.001098 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.797 | above 0 | yes |
| Calmar | 0.871 | above 0.75 | yes |
| Trades per day | 0.1921 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.209 % |
| Yearly return | +20.4 % (over 7.94 years) |
| Days in a position | 53 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-03.b2_rising-market-range-top-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
