---
backtest: N7-02_only-large-dips-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5912 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03703 | above 0 | yes |
| Mean daily return | 0.0006271 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4342 | above 0 | yes |
| Calmar | 0.4207 | above 0.75 | no |
| Trades per bar | 0.1123 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N7-02_only-large-dips-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
