---
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6014 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.0477 | above 0 | yes |
| Mean daily return | 0.0008566 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.45 | above 0 | yes |
| Calmar | 0.3274 | above 0.75 | no |
| Trades per day | 0.3893 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
