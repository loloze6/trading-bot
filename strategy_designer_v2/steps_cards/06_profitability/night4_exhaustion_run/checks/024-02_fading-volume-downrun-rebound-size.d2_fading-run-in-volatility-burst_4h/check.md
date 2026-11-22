---
backtest: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6319 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07812 | above 0 | yes |
| Mean daily return | 0.0007171 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4682 | above 0 | yes |
| Calmar | 0.3882 | above 0.75 | no |
| Trades per day | 0.4286 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
