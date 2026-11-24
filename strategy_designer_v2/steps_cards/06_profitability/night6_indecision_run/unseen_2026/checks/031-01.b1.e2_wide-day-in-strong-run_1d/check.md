---
backtest: 031-01.b1.e2_wide-day-in-strong-run_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7224 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6243 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007607 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.7929 | above 0 | no |
| Calmar | 0.8304 | above 0.75 | yes |
| Trades per day | 0.2227 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.297 % |
| Yearly return | +16.2 % (over 0.87 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.e2_wide-day-in-strong-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
