---
backtest: 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2989 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8647 | above 0 | no |
| Mean daily return | -0.0001009 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4872 | above 0 | no |
| Calmar | -0.1265 | above 0.75 | no |
| Trades per day | 0.0139 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
