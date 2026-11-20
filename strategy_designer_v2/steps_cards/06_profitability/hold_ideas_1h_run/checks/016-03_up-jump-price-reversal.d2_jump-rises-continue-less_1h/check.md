---
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8747 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.321 | above 0 | yes |
| Mean daily return | 0.00093 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7223 | above 0 | yes |
| Calmar | 0.6451 | above 0.75 | no |
| Trades per day | 0.3154 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/hold_ideas_1h_run/backtests/016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
