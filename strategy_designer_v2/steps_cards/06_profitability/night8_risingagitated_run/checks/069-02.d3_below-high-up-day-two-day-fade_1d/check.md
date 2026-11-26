---
backtest: 069-02.d3_below-high-up-day-two-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.02336 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5308 | above 0 | no |
| Mean daily return, on days in a position | 2.123e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1268 | above 0 | no |
| Calmar | -0.05007 | above 0.75 | no |
| Trades per day | 0.3149 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.385 % |
| Yearly return | -2.8 % (over 7.94 years) |
| Days in a position | 80 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d3_below-high-up-day-two-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
