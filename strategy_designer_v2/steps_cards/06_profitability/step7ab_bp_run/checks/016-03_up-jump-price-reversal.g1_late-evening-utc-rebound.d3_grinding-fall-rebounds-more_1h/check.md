---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7243 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1706 | above 0 | yes |
| Mean daily return | 0.0006479 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5676 | above 0 | yes |
| Calmar | 0.5514 | above 0.75 | no |
| Trades per day | 0.5732 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
