---
backtest: N5-02_high-below-60-day-fails_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5947 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.149 | above 0 | no |
| Mean daily return | -0.0004642 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.692 | above 0 | no |
| Calmar | -0.2212 | above 0.16 | no |
| Trades per bar | 0.08525 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N5-02_high-below-60-day-fails_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
