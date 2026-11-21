---
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3458 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2084 | above 0 | no |
| Mean daily return | 0.0002733 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1535 | above 0 | yes |
| Calmar | 0.1285 | above 0.75 | no |
| Trades per day | 0.07333 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
