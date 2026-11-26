---
backtest: 041-02_wide-down-day-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7715 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2173 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008016 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6251 | above 0 | yes |
| Calmar | 0.752 | above 0.75 | yes |
| Trades per day | 0.4072 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.489 % |
| Yearly return | +19.5 % (over 7.94 years) |
| Days in a position | 75 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/backtests/041-02_wide-down-day-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
