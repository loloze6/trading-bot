---
backtest: 032-02.b1.e1.e1.e3_two-month-momentum-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1147 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4394 | above 0 | no |
| Mean daily return, on days in a position | 0.000128 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.04247 | above 0 | no |
| Calmar | -0.04593 | above 0.75 | no |
| Trades per day | 0.1722 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.127 % |
| Yearly return | -3.6 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e3_two-month-momentum-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
