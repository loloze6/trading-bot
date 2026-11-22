---
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1727 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3811 | above 0 | no |
| Mean daily return | 6.166e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.0612 | above 0 | yes |
| Calmar | 0.07254 | above 0.75 | no |
| Trades per day | 0.2227 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
