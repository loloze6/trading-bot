---
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -4.279 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.833 | above 0 | no |
| Mean daily return | -0.001 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -4.8 | above 0 | no |
| Calmar | -0.326 | above 0.75 | no |
| Trades per day | 0.8575 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
