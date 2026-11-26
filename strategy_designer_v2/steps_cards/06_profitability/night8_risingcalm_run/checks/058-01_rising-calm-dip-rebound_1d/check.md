---
backtest: 058-01_rising-calm-dip-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5769 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.007268 | above 0 | yes |
| Mean daily return, on days in a position | 0.001121 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4555 | above 0 | yes |
| Calmar | 0.393 | above 0.75 | no |
| Trades per day | 0.05739 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.533 % |
| Yearly return | +5.5 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-01_rising-calm-dip-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
