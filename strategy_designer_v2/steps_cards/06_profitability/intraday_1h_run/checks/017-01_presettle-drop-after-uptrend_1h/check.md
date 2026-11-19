---
backtest: 017-01_presettle-drop-after-uptrend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -5.032 | above 0 | no |
| Sharpe minus holding's Sharpe | -5.586 | above 0 | no |
| Mean daily return | -0.001813 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -5.354 | above 0 | no |
| Calmar | -0.4912 | above 0.75 | no |
| Trades per day | 1.8 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-01_presettle-drop-after-uptrend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
