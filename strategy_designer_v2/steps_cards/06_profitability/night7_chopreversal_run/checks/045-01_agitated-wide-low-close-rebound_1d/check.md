---
backtest: 045-01_agitated-wide-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9146 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.345 | above 0 | yes |
| Mean daily return, on days in a position | 0.001105 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.77 | above 0 | yes |
| Calmar | 0.9635 | above 0.75 | yes |
| Trades per day | 0.3282 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.149 % |
| Yearly return | +19.3 % (over 7.94 years) |
| Days in a position | 50 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/045-01_agitated-wide-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
