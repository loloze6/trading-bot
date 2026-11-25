---
backtest: 038-02_rising-market-range-scaled-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.041 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4872 | above 0 | yes |
| Mean daily return, on days in a position | 0.001489 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8218 | above 0 | yes |
| Calmar | 0.7157 | above 0.75 | no |
| Trades per day | 0.1581 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.065 % |
| Yearly return | +21.1 % (over 7.94 years) |
| Days in a position | 39 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/038-02_rising-market-range-scaled-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
