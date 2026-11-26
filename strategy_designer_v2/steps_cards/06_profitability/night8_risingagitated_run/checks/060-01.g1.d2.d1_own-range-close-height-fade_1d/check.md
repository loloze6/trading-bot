---
backtest: 060-01.g1.d2.d1_own-range-close-height-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6857 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1161 | above 0 | yes |
| Mean daily return, on days in a position | 0.00274 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5034 | above 0 | yes |
| Calmar | 0.8063 | above 0.75 | yes |
| Trades per day | 0.01853 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.274 % |
| Yearly return | +3.5 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d2.d1_own-range-close-height-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
