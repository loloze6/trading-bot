---
backtest: 002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5479 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.02029 | above 0 | no |
| Mean daily return | 0.0004087 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2615 | above 0 | yes |
| Calmar | 0.233 | above 0.75 | no |
| Trades per bar | 0.03212 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
