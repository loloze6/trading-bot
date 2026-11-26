---
backtest: 032-02.g1_uptrend-near-high-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.069 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5144 | above 0 | yes |
| Mean daily return, on days in a position | 0.001431 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.883 | above 0 | yes |
| Calmar | 0.9513 | above 0.75 | yes |
| Trades per day | 0.1949 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.666 % |
| Yearly return | +33.6 % (over 7.94 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1_uptrend-near-high-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
