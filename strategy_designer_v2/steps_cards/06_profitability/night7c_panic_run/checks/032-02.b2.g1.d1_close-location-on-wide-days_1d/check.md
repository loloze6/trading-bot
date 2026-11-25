---
backtest: 032-02.b2.g1.d1_close-location-on-wide-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.09509 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4591 | above 0 | no |
| Mean daily return, on days in a position | 9.097e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.00913 | above 0 | no |
| Calmar | -0.04701 | above 0.75 | no |
| Trades per day | 0.8773 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.824 % |
| Yearly return | -2.8 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1.d1_close-location-on-wide-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
