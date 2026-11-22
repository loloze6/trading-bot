---
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1919 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7461 | above 0 | no |
| Mean daily return | -4.971e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3353 | above 0 | no |
| Calmar | -0.09654 | above 0.75 | no |
| Trades per day | 0.1041 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
