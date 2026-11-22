---
backtest: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8268 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2726 | above 0 | yes |
| Mean daily return | 0.0006434 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5977 | above 0 | yes |
| Calmar | 0.5291 | above 0.75 | no |
| Trades per day | 0.1286 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
