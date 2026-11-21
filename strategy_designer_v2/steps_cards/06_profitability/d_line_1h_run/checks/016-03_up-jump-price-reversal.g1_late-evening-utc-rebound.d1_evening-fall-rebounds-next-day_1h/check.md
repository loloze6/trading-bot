---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.237 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.79 | above 0 | no |
| Mean daily return | -0.0004082 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.396 | above 0 | no |
| Calmar | -0.2 | above 0.75 | no |
| Trades per day | 0.413 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
