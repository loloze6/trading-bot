---
backtest: 060-01.g1.d2.d1_own-range-close-height-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.22 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.122 | above 0 | yes |
| Mean daily return, on days in a position | 0.002781 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1118 | above 0 | no |
| Calmar | 2.593 | above 0.75 | yes |
| Trades per day | 0.02596 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.219 % |
| Yearly return | +5.2 % (over 0.87 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_2026/backtests/060-01.g1.d2.d1_own-range-close-height-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
