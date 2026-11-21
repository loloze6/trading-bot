---
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.05 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.604 | above 0 | no |
| Mean daily return | -0.0002566 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.241 | above 0 | no |
| Calmar | -0.1701 | above 0.75 | no |
| Trades per day | 0.7668 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
