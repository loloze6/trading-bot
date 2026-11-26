---
backtest: 032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.203 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6489 | above 0 | yes |
| Mean daily return, on days in a position | 0.004145 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.029 | above 0 | yes |
| Calmar | 1.466 | above 0.75 | yes |
| Trades per day | 0.01295 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.047 % |
| Yearly return | +24.7 % (over 7.94 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
