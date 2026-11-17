---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6585 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1043 | above 0 | yes |
| Mean daily return | 0.000506 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5073 | above 0 | yes |
| Calmar | 0.5542 | above 0.75 | no |
| Trades per bar | 0.3934 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
