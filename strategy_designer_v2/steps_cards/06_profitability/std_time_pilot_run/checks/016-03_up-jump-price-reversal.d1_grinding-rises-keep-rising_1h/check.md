---
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8772 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3235 | above 0 | yes |
| Mean daily return | 0.000946 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7104 | above 0 | yes |
| Calmar | 0.6345 | above 0.75 | no |
| Trades per day | 0.337 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/std_time_pilot_run/backtests/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
