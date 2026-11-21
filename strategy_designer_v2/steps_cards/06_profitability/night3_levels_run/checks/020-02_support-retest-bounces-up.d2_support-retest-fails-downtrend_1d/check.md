---
backtest: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2226 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7768 | above 0 | no |
| Mean daily return | -0.000112 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3691 | above 0 | no |
| Calmar | -0.08976 | above 0.75 | no |
| Trades per day | 0.09804 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
