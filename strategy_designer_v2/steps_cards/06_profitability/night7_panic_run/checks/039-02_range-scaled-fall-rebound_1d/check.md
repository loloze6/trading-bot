---
backtest: 039-02_range-scaled-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7243 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1701 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007761 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5735 | above 0 | yes |
| Calmar | 0.6274 | above 0.75 | no |
| Trades per day | 0.3928 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.447 % |
| Yearly return | +17.5 % (over 7.94 years) |
| Days in a position | 71 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/039-02_range-scaled-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
