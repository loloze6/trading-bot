---
backtest: 032-02.b2.g2.d3_rebound-scaled-by-range-widening_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7084 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1543 | above 0 | yes |
| Mean daily return, on days in a position | 0.001136 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6145 | above 0 | yes |
| Calmar | 0.5874 | above 0.75 | no |
| Trades per day | 0.3641 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.513 % |
| Yearly return | +17.7 % (over 7.94 years) |
| Days in a position | 49 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g2.d3_rebound-scaled-by-range-widening_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
