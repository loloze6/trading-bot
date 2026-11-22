---
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -3.738 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.292 | above 0 | no |
| Mean daily return | -0.001004 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -3.927 | above 0 | no |
| Calmar | -0.327 | above 0.75 | no |
| Trades per day | 1.425 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
