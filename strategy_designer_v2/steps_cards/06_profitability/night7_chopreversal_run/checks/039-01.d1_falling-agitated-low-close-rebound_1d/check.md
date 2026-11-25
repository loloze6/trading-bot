---
backtest: 039-01.d1_falling-agitated-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.979 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4094 | above 0 | yes |
| Mean daily return, on days in a position | 0.0002819 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7873 | above 0 | yes |
| Calmar | 0.6421 | above 0.75 | no |
| Trades per day | 0.1061 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.160 % |
| Yearly return | +3.0 % (over 7.94 years) |
| Days in a position | 29 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/039-01.d1_falling-agitated-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
