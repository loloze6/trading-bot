---
backtest: 058-03_calm-rise-stretch-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9737 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4041 | above 0 | yes |
| Mean daily return, on days in a position | 0.002769 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8121 | above 0 | yes |
| Calmar | 0.8299 | above 0.75 | yes |
| Trades per day | 0.06217 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.910 % |
| Yearly return | +16.7 % (over 7.94 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03_calm-rise-stretch-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
