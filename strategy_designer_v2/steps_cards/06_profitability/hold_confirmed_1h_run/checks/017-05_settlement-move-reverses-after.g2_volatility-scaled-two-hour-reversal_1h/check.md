---
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -6.737 | above 0 | no |
| Sharpe minus holding's Sharpe | -7.291 | above 0 | no |
| Mean daily return | -0.005294 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -7.074 | above 0 | no |
| Calmar | -0.8619 | above 0.75 | no |
| Trades per day | 13.27 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
