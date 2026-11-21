---
backtest: 020-02_support-retest-bounces-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.0003385 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5538 | above 0 | no |
| Mean daily return | 3.308e-07 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1384 | above 0 | no |
| Calmar | -0.1012 | above 0.75 | no |
| Trades per day | 0.1234 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
