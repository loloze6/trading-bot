---
backtest: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5752 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.129 | above 0 | no |
| Mean daily return | -0.0003852 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7278 | above 0 | no |
| Calmar | -0.1956 | above 0.75 | no |
| Trades per bar | 0.4278 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
