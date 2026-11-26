---
backtest: 061-01.d2_rising-calm-up-day-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8838 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3142 | above 0 | yes |
| Mean daily return, on days in a position | 0.002507 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.724 | above 0 | yes |
| Calmar | 0.6113 | above 0.75 | no |
| Trades per day | 0.0666 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.188 % |
| Yearly return | +19.2 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.d2_rising-calm-up-day-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
