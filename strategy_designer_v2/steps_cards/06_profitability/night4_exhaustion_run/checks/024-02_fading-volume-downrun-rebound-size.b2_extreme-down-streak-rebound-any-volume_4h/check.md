---
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7276 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1739 | above 0 | yes |
| Mean daily return | 0.001364 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5822 | above 0 | yes |
| Calmar | 0.4304 | above 0.75 | no |
| Trades per day | 0.2149 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
