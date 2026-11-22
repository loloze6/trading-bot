---
backtest: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.063 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5093 | above 0 | yes |
| Mean daily return | 0.001418 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.877 | above 0 | yes |
| Calmar | 1.089 | above 0.75 | yes |
| Trades per day | 0.1151 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
