---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4969 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05679 | above 0 | no |
| Mean daily return | 0.000368 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3685 | above 0 | yes |
| Calmar | 0.1893 | above 0.75 | no |
| Trades per day | 0.3912 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/d_line_1h_v2_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
