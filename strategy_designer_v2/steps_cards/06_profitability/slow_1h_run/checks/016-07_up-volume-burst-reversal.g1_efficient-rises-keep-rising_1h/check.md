---
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7158 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.27 | above 0 | no |
| Mean daily return | -0.0004601 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8853 | above 0 | no |
| Calmar | -0.223 | above 0.75 | no |
| Trades per day | 3.154 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
