---
backtest: N2-02_capitulation-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6137 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.04405 | above 0 | yes |
| Mean daily return | 0.0004649 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3841 | above 0 | yes |
| Calmar | 0.3929 | above 0.1811 | yes |
| Trades per bar | 0.03012 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-02_capitulation-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
