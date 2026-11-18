---
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1019 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4523 | above 0 | no |
| Mean daily return | 4.904e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.09036 | above 0 | no |
| Calmar | 0.005748 | above 0.75 | no |
| Trades per bar | 0.1662 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/volume_run/backtests/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
