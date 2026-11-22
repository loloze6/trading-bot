---
backtest: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.046 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.6 | above 0 | no |
| Mean daily return | -0.001048 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.178 | above 0 | no |
| Calmar | -0.3429 | above 0.75 | no |
| Trades per day | 1.893 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
