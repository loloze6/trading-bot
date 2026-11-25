---
backtest: 034-01.d1_wide-range-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8737 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3041 | above 0 | yes |
| Mean daily return, on days in a position | 0.001105 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7479 | above 0 | yes |
| Calmar | 0.9044 | above 0.75 | yes |
| Trades per day | 0.3227 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.202 % |
| Yearly return | +19.0 % (over 7.94 years) |
| Days in a position | 50 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/034-01.d1_wide-range-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
