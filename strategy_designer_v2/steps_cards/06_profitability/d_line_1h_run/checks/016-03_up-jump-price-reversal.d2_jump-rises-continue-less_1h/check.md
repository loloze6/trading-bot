---
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.02 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.574 | above 0 | no |
| Mean daily return | -0.0005233 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.177 | above 0 | no |
| Calmar | -0.2297 | above 0.75 | no |
| Trades per day | 1.148 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
