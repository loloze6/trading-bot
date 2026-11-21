---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -16.35 | above 0 | no |
| Sharpe minus holding's Sharpe | -16.9 | above 0 | no |
| Mean daily return | -0.01362 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -16.86 | above 0 | no |
| Calmar | -0.9936 | above 0.75 | no |
| Trades per day | 20.77 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
