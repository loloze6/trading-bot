---
backtest: 032-02.b2.g2.d2_below-midrange-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7902 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.236 | above 0 | yes |
| Mean daily return, on days in a position | 0.0003036 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.679 | above 0 | yes |
| Calmar | 0.7633 | above 0.75 | yes |
| Trades per day | 0.112 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.242 % |
| Yearly return | +3.6 % (over 7.94 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g2.d2_below-midrange-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
