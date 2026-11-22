---
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1585 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7122 | above 0 | no |
| Mean daily return | -0.0002173 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2999 | above 0 | no |
| Calmar | -0.2044 | above 0.75 | no |
| Trades per day | 0.1809 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
