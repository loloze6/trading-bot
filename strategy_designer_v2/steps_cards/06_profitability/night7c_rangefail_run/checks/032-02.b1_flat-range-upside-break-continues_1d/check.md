---
backtest: 032-02.b1_flat-range-upside-break-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9349 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3807 | above 0 | yes |
| Mean daily return, on days in a position | 0.004141 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7459 | above 0 | yes |
| Calmar | 0.8952 | above 0.75 | yes |
| Trades per day | 0.02111 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.721 % |
| Yearly return | +12.7 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1_flat-range-upside-break-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
