---
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5159 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03823 | above 0 | no |
| Mean daily return | 0.0002864 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3337 | above 0 | yes |
| Calmar | 0.2698 | above 0.75 | no |
| Trades per bar | 0.4112 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
