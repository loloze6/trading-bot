---
backtest: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7019 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1482 | above 0 | yes |
| Mean daily return | 0.001321 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5468 | above 0 | yes |
| Calmar | 0.3666 | above 0.75 | no |
| Trades per day | 0.06819 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
