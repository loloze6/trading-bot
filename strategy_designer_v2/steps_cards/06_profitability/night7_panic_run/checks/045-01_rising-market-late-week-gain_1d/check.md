---
backtest: 045-01_rising-market-late-week-gain_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.088 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5339 | above 0 | yes |
| Mean daily return, on days in a position | 0.002621 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8831 | above 0 | yes |
| Calmar | 0.9671 | above 0.75 | yes |
| Trades per day | 0.07162 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.765 % |
| Yearly return | +16.0 % (over 7.94 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/backtests/045-01_rising-market-late-week-gain_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
