---
backtest: 022-02_combination-beats-best-single_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.8499 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.404 | above 0 | no |
| Mean daily return | -0.0006673 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.017 | above 0 | no |
| Calmar | -0.2721 | above 0.75 | no |
| Trades per day | 0.3808 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
