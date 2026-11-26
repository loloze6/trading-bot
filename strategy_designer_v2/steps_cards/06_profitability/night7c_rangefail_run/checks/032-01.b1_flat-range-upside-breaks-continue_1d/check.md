---
backtest: 032-01.b1_flat-range-upside-breaks-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5592 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.005078 | above 0 | yes |
| Mean daily return, on days in a position | 0.000548 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4242 | above 0 | yes |
| Calmar | 0.5145 | above 0.75 | no |
| Trades per day | 0.01153 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.395 % |
| Yearly return | +4.0 % (over 7.94 years) |
| Days in a position | 21 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-01.b1_flat-range-upside-breaks-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
