---
backtest: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.817 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.371 | above 0 | no |
| Mean daily return | -0.0005572 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.115 | above 0 | no |
| Calmar | -0.2317 | above 0.75 | no |
| Trades per day | 1.511 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
