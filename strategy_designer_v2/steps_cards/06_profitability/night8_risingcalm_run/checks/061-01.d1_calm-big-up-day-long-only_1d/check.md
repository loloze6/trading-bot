---
backtest: 061-01.d1_calm-big-up-day-long-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.606 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03642 | above 0 | yes |
| Mean daily return, on days in a position | 0.001052 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4388 | above 0 | yes |
| Calmar | 0.3092 | above 0.75 | no |
| Trades per day | 0.1666 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.808 % |
| Yearly return | +16.2 % (over 7.94 years) |
| Days in a position | 55 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.d1_calm-big-up-day-long-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
