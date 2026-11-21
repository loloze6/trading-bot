---
backtest: 017-03_postsettle-recovery-after-uptrend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -3.538 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.092 | above 0 | no |
| Mean daily return | -0.001259 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -3.899 | above 0 | no |
| Calmar | -0.3831 | above 0.75 | no |
| Trades per day | 1.832 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-03_postsettle-recovery-after-uptrend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
