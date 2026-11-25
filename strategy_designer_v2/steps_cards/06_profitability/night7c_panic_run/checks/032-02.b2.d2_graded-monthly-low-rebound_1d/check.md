---
backtest: 032-02.b2.d2_graded-monthly-low-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5125 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06911 | above 0 | no |
| Mean daily return, on days in a position | 0.002751 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4066 | above 0 | yes |
| Calmar | 0.2684 | above 0.75 | no |
| Trades per day | 0.01883 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.436 % |
| Yearly return | +4.0 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.d2_graded-monthly-low-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
