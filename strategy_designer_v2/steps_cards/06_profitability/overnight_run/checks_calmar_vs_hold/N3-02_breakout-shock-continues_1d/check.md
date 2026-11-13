---
backtest: N3-02_breakout-shock-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4153 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1388 | above 0 | no |
| Mean daily return | 0.000364 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1705 | above 0 | yes |
| Calmar | 0.1461 | above 0.16 | no |
| Trades per bar | 0.08742 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-02_breakout-shock-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
