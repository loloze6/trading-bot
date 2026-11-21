---
backtest: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.9699 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.524 | above 0 | no |
| Mean daily return | -0.0002434 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.092 | above 0 | no |
| Calmar | -0.1654 | above 0.75 | no |
| Trades per day | 0.6551 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
