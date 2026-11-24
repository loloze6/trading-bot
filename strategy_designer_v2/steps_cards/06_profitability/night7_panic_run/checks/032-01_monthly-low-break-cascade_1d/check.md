---
backtest: 032-01_monthly-low-break-cascade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.418 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9876 | above 0 | no |
| Mean daily return, on days in a position | -0.0006076 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7018 | above 0 | no |
| Calmar | -0.09169 | above 0.75 | no |
| Trades per day | 0.0162 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.326 % |
| Yearly return | -2.8 % (over 7.94 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/032-01_monthly-low-break-cascade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
