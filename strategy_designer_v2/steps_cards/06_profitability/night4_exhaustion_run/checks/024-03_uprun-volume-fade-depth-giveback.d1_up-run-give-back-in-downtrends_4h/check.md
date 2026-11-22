---
backtest: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.08939 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6431 | above 0 | no |
| Mean daily return | -0.000106 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2443 | above 0 | no |
| Calmar | -0.1545 | above 0.75 | no |
| Trades per day | 0.1541 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
