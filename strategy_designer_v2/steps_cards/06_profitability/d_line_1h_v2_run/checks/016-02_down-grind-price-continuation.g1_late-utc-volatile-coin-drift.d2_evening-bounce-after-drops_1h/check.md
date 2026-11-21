---
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6662 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.22 | above 0 | no |
| Mean daily return | -0.0001422 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9022 | above 0 | no |
| Calmar | -0.1314 | above 0.75 | no |
| Trades per day | 0.408 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/d_line_1h_v2_run/backtests/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
