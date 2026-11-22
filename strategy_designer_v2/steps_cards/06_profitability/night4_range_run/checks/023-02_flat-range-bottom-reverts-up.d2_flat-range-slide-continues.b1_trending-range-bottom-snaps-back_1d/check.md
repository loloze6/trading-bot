---
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2013 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3529 | above 0 | no |
| Mean daily return | 0.0001183 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1455 | above 0 | yes |
| Calmar | 0.04809 | above 0.75 | no |
| Trades per day | 0.09695 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
