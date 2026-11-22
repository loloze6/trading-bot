---
backtest: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3112 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8653 | above 0 | no |
| Mean daily return | -7.654e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4764 | above 0 | no |
| Calmar | -0.1038 | above 0.75 | no |
| Trades per day | 0.07647 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
