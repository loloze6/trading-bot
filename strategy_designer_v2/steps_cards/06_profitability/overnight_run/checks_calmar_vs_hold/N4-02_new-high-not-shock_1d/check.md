---
backtest: N4-02_new-high-not-shock_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4377 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1165 | above 0 | no |
| Mean daily return | 0.0003714 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2386 | above 0 | yes |
| Calmar | 0.1706 | above 0.16 | yes |
| Trades per bar | 0.1035 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-02_new-high-not-shock_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
