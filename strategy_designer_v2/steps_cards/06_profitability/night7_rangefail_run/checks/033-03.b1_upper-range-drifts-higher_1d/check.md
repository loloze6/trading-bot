---
backtest: 033-03.b1_upper-range-drifts-higher_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8031 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2489 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006599 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6409 | above 0 | yes |
| Calmar | 0.5354 | above 0.75 | no |
| Trades per day | 0.2789 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.567 % |
| Yearly return | +21.6 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-03.b1_upper-range-drifts-higher_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
