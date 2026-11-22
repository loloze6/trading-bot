---
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5698 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01559 | above 0 | yes |
| Mean daily return | 8.819e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.421 | above 0 | yes |
| Calmar | 0.3735 | above 0.75 | no |
| Trades per day | 0.0311 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
