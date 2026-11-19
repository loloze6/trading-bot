---
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.549 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.103 | above 0 | no |
| Mean daily return | -0.0006204 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.71 | above 0 | no |
| Calmar | -0.2442 | above 0.75 | no |
| Trades per day | 0.6321 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
