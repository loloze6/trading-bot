---
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6773 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1231 | above 0 | yes |
| Mean daily return | 0.0004359 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4797 | above 0 | yes |
| Calmar | 0.2581 | above 0.75 | no |
| Trades per day | 0.1587 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
