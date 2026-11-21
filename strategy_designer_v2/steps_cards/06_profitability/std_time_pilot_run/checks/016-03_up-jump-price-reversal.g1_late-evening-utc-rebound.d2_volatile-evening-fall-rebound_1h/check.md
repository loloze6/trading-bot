---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.175 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6215 | above 0 | yes |
| Mean daily return | 0.0006646 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.067 | above 0 | yes |
| Calmar | 0.6944 | above 0.75 | no |
| Trades per day | 0.3331 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/std_time_pilot_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
