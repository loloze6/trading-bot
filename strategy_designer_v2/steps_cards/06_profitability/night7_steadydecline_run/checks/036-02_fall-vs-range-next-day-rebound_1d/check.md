---
backtest: 036-02_fall-vs-range-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.484 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.07017 | above 0 | no |
| Mean daily return, on days in a position | 0.002245 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3751 | above 0 | yes |
| Calmar | 0.3586 | above 0.75 | no |
| Trades per day | 0.0493 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.906 % |
| Yearly return | +7.1 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/036-02_fall-vs-range-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
