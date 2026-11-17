---
backtest: 012-02_volume-burst-fall-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2342 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3199 | above 0 | no |
| Mean daily return | 8.189e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1413 | above 0 | yes |
| Calmar | 0.107 | above 0.75 | no |
| Trades per bar | 0.02693 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/volume_run/backtests/012-02_volume-burst-fall-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
