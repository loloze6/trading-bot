---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.256 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.811 | above 0 | no |
| Mean daily return | -0.00075 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.346 | above 0 | no |
| Calmar | -0.2793 | above 0.75 | no |
| Trades per bar | 0.1568 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
