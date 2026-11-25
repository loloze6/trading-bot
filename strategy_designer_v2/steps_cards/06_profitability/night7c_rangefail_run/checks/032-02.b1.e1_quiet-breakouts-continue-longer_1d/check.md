---
backtest: 032-02.b1.e1_quiet-breakouts-continue-longer_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.071 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.517 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009895 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8681 | above 0 | yes |
| Calmar | 1.229 | above 0.75 | yes |
| Trades per day | 0.02545 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.429 % |
| Yearly return | +8.8 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1_quiet-breakouts-continue-longer_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
