---
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4631 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.017 | above 0 | no |
| Mean daily return | -0.0005876 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6146 | above 0 | no |
| Calmar | -0.2913 | above 0.75 | no |
| Trades per day | 0.1475 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
