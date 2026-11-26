---
backtest: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4997 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4017 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007074 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2512 | above 0 | yes |
| Calmar | 0.9947 | above 0.75 | yes |
| Trades per day | 0.03894 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.211 % |
| Yearly return | +1.9 % (over 0.87 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2026/backtests/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
