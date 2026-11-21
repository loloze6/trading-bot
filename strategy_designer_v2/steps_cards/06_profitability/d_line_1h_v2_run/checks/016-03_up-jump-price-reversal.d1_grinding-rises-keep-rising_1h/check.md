---
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.876 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3223 | above 0 | yes |
| Mean daily return | 0.0007058 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7406 | above 0 | yes |
| Calmar | 0.8739 | above 0.75 | yes |
| Trades per day | 0.1223 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/d_line_1h_v2_run/backtests/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
