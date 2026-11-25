---
backtest: 032-03_deep-fall-low-exhaustion-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2772 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2924 | above 0 | no |
| Mean daily return, on days in a position | 0.0007181 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1642 | above 0 | yes |
| Calmar | 0.1347 | above 0.75 | no |
| Trades per day | 0.02727 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.535 % |
| Yearly return | +2.3 % (over 7.94 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-03_deep-fall-low-exhaustion-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
