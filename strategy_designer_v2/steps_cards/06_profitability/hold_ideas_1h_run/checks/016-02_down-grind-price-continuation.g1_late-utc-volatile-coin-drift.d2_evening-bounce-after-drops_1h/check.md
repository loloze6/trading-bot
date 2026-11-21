---
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3909 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9447 | above 0 | no |
| Mean daily return | -8.766e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5986 | above 0 | no |
| Calmar | -0.08152 | above 0.75 | no |
| Trades per day | 0.6513 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_ideas_1h_run/backtests/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
