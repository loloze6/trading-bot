---
backtest: 003-02_thin-volume-drop-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5981 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.04394 | above 0 | yes |
| Mean daily return | 3.604e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5043 | above 0 | yes |
| Calmar | 11.99 | above 0.75 | yes |
| Trades per bar | 0.0002853 | at least 0.01 | no |

- Decided by: failed: Mean daily return; Trades per bar
Record: `steps_cards/04_backtest/volume_run/backtests/003-02_thin-volume-drop-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
