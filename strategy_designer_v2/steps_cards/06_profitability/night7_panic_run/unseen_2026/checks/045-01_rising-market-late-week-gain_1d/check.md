---
backtest: 045-01_rising-market-late-week-gain_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.006 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.9083 | above 0 | yes |
| Mean daily return, on days in a position | 0.002633 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2001 | above 0 | yes |
| Calmar | 1.663 | above 0.75 | yes |
| Trades per day | 0.06542 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.724 % |
| Yearly return | +13.9 % (over 0.87 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2026/backtests/045-01_rising-market-late-week-gain_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
