---
backtest: 032-01_flat-range-upside-break-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5594 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.114 | above 0 | no |
| Mean daily return, on days in a position | -0.0005367 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6394 | above 0 | no |
| Calmar | -0.1234 | above 0.75 | no |
| Trades per day | 0.01324 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.316 % |
| Yearly return | -3.5 % (over 7.94 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-01_flat-range-upside-break-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
