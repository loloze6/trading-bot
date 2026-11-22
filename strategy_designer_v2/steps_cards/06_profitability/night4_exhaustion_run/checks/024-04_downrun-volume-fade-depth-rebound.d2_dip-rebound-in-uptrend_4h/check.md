---
backtest: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.047 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4937 | above 0 | yes |
| Mean daily return | 0.001319 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.874 | above 0 | yes |
| Calmar | 0.9937 | above 0.75 | yes |
| Trades per day | 0.1659 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
