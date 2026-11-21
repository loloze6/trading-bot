---
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.0008411 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.555 | above 0 | no |
| Mean daily return | -3.809e-07 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4313 | above 0 | no |
| Calmar | -0.02699 | above 0.75 | no |
| Trades per day | 0.03002 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
