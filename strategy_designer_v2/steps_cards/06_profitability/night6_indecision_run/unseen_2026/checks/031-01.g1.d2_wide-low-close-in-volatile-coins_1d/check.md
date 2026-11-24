---
backtest: 031-01.g1.d2_wide-low-close-in-volatile-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.195 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.097 | above 0 | yes |
| Mean daily return, on days in a position | 0.01023 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8443 | above 0 | yes |
| Calmar | 3.824 | above 0.75 | yes |
| Trades per day | 0.02285 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.764 % |
| Yearly return | +17.9 % (over 0.87 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.g1.d2_wide-low-close-in-volatile-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
