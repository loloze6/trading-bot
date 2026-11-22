---
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6619 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.216 | above 0 | no |
| Mean daily return | -0.0002913 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7612 | above 0 | no |
| Calmar | -0.161 | above 0.75 | no |
| Trades per day | 0.2189 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
