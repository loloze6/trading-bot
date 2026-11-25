---
backtest: 032-02.b2_volatile-low-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6469 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07733 | above 0 | yes |
| Mean daily return, on days in a position | 0.007 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5093 | above 0 | yes |
| Calmar | 1.719 | above 0.75 | yes |
| Trades per day | 0.002738 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.122 % |
| Yearly return | +1.5 % (over 7.94 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Trades per day
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2_volatile-low-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
