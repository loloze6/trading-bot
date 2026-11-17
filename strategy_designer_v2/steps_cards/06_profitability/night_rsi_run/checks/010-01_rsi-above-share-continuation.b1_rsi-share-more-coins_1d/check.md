---
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3335 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2207 | above 0 | no |
| Mean daily return | 0.0003249 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2044 | above 0 | yes |
| Calmar | 0.09926 | above 0.75 | no |
| Trades per bar | 0.1896 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
