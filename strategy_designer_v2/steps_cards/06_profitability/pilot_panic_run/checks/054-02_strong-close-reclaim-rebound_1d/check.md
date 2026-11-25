---
backtest: 054-02_strong-close-reclaim-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1936 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.376 | above 0 | no |
| Mean daily return, on days in a position | 0.0019 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.03428 | above 0 | yes |
| Calmar | 0.1489 | above 0.75 | no |
| Trades per day | 0.007108 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.464 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-02_strong-close-reclaim-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
