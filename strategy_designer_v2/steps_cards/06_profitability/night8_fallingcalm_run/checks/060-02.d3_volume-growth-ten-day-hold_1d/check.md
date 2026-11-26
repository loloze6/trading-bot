---
backtest: 060-02.d3_volume-growth-ten-day-hold_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6932 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.139 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008367 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5364 | above 0 | yes |
| Calmar | 0.4063 | above 0.75 | no |
| Trades per day | 0.07921 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.869 % |
| Yearly return | +10.7 % (over 7.94 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d3_volume-growth-ten-day-hold_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
