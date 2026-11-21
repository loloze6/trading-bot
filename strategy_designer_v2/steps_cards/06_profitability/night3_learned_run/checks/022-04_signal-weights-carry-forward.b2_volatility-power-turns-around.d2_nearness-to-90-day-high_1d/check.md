---
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4421 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.112 | above 0 | no |
| Mean daily return | 0.0001094 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3455 | above 0 | yes |
| Calmar | 0.2163 | above 0.75 | no |
| Trades per day | 0.07778 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
