---
backtest: 032-02.b2.g1.d2_long-reversal-after-wide-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7617 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2075 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008152 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6112 | above 0 | yes |
| Calmar | 0.5397 | above 0.75 | no |
| Trades per day | 0.7406 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.037 % |
| Yearly return | +24.6 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1.d2_long-reversal-after-wide-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
