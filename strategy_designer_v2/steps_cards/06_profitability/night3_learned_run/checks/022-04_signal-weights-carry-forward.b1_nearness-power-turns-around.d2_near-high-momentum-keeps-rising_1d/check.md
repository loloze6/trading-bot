---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4237 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1305 | above 0 | no |
| Mean daily return | 0.0002041 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3328 | above 0 | yes |
| Calmar | 0.1916 | above 0.75 | no |
| Trades per day | 0.2196 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
