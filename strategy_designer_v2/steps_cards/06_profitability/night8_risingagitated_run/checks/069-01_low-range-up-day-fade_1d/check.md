---
backtest: 069-01_low-range-up-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3336 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2206 | above 0 | no |
| Mean daily return, on days in a position | 0.0003813 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1586 | above 0 | yes |
| Calmar | 0.1614 | above 0.75 | no |
| Trades per day | 0.1649 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.699 % |
| Yearly return | +3.6 % (over 7.94 years) |
| Days in a position | 32 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-01_low-range-up-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
