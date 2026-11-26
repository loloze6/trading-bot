---
backtest: 060-01.g1.d2.g1_up-day-high-close-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3536 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.216 | above 0 | no |
| Mean daily return, on days in a position | 0.0008161 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1907 | above 0 | yes |
| Calmar | 0.1846 | above 0.75 | no |
| Trades per day | 0.0543 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.459 % |
| Yearly return | +2.8 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d2.g1_up-day-high-close-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
