---
backtest: 002-01_sma-golden-cross-upward-drift_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4894 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.08021 | above 0 | no |
| Mean daily return | 0.0003773 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2089 | above 0 | yes |
| Calmar | 0.2015 | above 0.75 | no |
| Trades per bar | 0.03298 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/full_data_run/backtests/002-01_sma-golden-cross-upward-drift_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
