---
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.298 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.852 | above 0 | no |
| Mean daily return | -0.002347 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.402 | above 0 | no |
| Calmar | -0.6062 | above 0.75 | no |
| Trades per day | 10.61 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
