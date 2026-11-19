---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -14.16 | above 0 | no |
| Sharpe minus holding's Sharpe | -14.71 | above 0 | no |
| Mean daily return | -0.01269 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -14.56 | above 0 | no |
| Calmar | -0.9911 | above 0.75 | no |
| Trades per day | 20.42 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
