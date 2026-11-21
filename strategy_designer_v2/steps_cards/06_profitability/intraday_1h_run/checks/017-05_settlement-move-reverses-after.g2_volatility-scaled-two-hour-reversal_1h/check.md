---
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -8.676 | above 0 | no |
| Sharpe minus holding's Sharpe | -9.23 | above 0 | no |
| Mean daily return | -0.00803 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -8.978 | above 0 | no |
| Calmar | -0.9503 | above 0.75 | no |
| Trades per day | 18.73 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
