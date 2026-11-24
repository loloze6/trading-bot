---
backtest: 031-02.b1.b2_flat-day-after-strong-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.252 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.154 | above 0 | yes |
| Mean daily return, on days in a position | 0.00374 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.038 | above 0 | yes |
| Calmar | 2.793 | above 0.75 | yes |
| Trades per day | 0.01506 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.542 % |
| Yearly return | +13.2 % (over 0.87 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b2_flat-day-after-strong-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
