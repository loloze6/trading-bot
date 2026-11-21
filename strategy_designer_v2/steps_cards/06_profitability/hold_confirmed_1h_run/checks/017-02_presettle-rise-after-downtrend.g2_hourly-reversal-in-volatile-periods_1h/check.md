---
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -10.69 | above 0 | no |
| Sharpe minus holding's Sharpe | -11.24 | above 0 | no |
| Mean daily return | -0.007737 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -11.14 | above 0 | no |
| Calmar | -0.9433 | above 0.75 | no |
| Trades per day | 12.94 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
