---
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7567 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.203 | above 0 | yes |
| Mean daily return | 0.0002521 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5307 | above 0 | yes |
| Calmar | 0.4721 | above 0.75 | no |
| Trades per day | 0.149 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
